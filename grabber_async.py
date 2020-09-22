import argparse
import requests
import os
from datetime import datetime
import json
import time
import gzip

import Database as db

from urllib3.exceptions import ReadTimeoutError

from dotenv import load_dotenv
load_dotenv()

import trio


def get_path_list():
    path_list = []
    url = "http://bustime.mta.info/api/where/routes-for-agency/MTA%20NYCT.json?key=" + os.getenv("API_KEY")

    try:
        response = requests.get(url, timeout=30)
    except ReadTimeoutError: # bug this doesnt seem to work
        print('Could not retrieve route definitions. OneBusAway API probably overloaded.')

    try:
        routes = response.json() # bug need to handle 503 errors here—load route definitions from the data/path_list.json file
    except:
        print("need to handle 503 errors here")
        pass

    print('Found {} routes. Fetching current positions with ASYNCHRONOUS requests...'.format(len(routes['data']['list'])))

    for route in routes['data']['list']:
        path_list.append({route['id']:"/api/siri/vehicle-monitoring.json?key={}&VehicleMonitoringDetailLevel=calls&LineRef={}".format(os.getenv("API_KEY"), route['id'])})

    # dump the list of routes json file
    with open((filepath() +'path_list.json'), 'w') as json_file:
       json.dump(path_list, json_file, indent=4) # use json.dumps ?

    return path_list

def dump_to_screen(feeds):
    for route_bundle in feeds:
        for route_id, data in route_bundle.items():
            print (data.json())
    return

def filepath():
    path = ("data/")
    check = os.path.isdir(path)
    if not check:
        os.makedirs(path)
        print("created folder : ", path)
    else:
        pass
    return path

def dump_to_file(feeds):
    timestamp_pretty = datetime.now().strftime("%Y-%m-%dT_%H:%M:%S.%f")
    for route_bundle in feeds:
        for route_id,route_report in route_bundle.items():
            dumpfile=(filepath() + route_id.split()[1] + '_' + timestamp_pretty +'.gz')
            with gzip.open(dumpfile, 'wt', encoding="ascii") as zipfile:
                json.dump(route_report.json(), zipfile)
    return timestamp

def dump_to_db(dbparams,timestamp, feeds):

    session,db_url = db.get_session(dbparams)
    print('Dumping to {}'.format(db_url))
    for route_bundle in feeds:
        for route_id,route_report in route_bundle.items():
            buses = db.parse_buses(timestamp, route_id, route_report.json(), db_url)
            for bus in buses:
                session.add(bus)
        session.commit()
    return




if __name__ == "__main__":
    start = time.time()

    # future this stuff shouldn't be hard-coded both here and in docker-compose.yml—load from a config.py or .env
    dbparams = {
        'dbname': 'buses',
        'dbuser': 'nycbuswatcher',
        'dbpassword': 'bustime',
        'dbhost':'localhost'
    }


    parser = argparse.ArgumentParser(description='NYCbuswatcher grabber, fetches and stores current position for buses')
    parser.add_argument('-p', action="store_true", dest="production")
    args = parser.parse_args()


    # # todo add scheduler
    # from apscheduler.schedulers.background import BackgroundScheduler

    print('NYC MTA BusTime API Scraper v0.1. Anthony Townsend <atownsend@cornell.edu>')

    if args.production is True:
        print('PRODUCTION MODE')
        connections=20
        dbparams['dbhost']='mysql_docker'

        # interval = 60
        # print('Scanning on {}-second interval.'.format(interval))
        # scheduler = BackgroundScheduler()
        # scheduler.add_job(get_buses, 'interval', seconds=interval,args=[dbparams])
        # scheduler.start()
        # try:
        #     while True:
        #         time.sleep(2)
        # except (KeyboardInterrupt, SystemExit):
        #     scheduler.shutdown()

    elif args.production is False: #run once and quit
        print('development MODE')
        connections=5
        dbparams['dbhost']='localhost'

    path_list = get_path_list()

    feeds = []

    async def grabber(s,a_path,route_id):
        r = await s.get(path=a_path)
        feeds.append({route_id:r})

    async def main(path_list):
        from asks.sessions import Session
        s = Session('http://bustime.mta.info', connections=connections)
        async with trio.open_nursery() as n:
            for path_bundle in path_list:
                for route_id,path in path_bundle.items():
                    n.start_soon(grabber, s, path, route_id )

    trio.run(main, path_list)

    # dump_to_screen(feeds)
    timestamp = dump_to_file(feeds)
    dump_to_db(dbparams,timestamp, feeds)

    end = time.time()
    print('\nFetched {} routes in {:2f} seconds to uncompressed archive and database.'.format(len(feeds),(end - start)))

