import argparse
import requests
import os
from datetime import datetime
import json
import time
import gzip
import pickle

import Database as db


from dotenv import load_dotenv
load_dotenv()

import trio


def get_path_list():
    path_list = []
    url = "http://bustime.mta.info/api/where/routes-for-agency/MTA%20NYCT.json?key=" + os.getenv("API_KEY")

    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 503: # response is bad, so go to exception and load the pickle
            raise Exception(503, "503 error code fetching route definitions. OneBusAway API probably overloaded.")
        else: # response is good, so save it to pickle and proceed
            with open((filepath() + 'routes-for-agency.pickle'), "wb") as pickle_file:
                pickle.dump(response,pickle_file)
    except Exception as e: # response is bad, so load the last good pickle
        with open((filepath() + 'routes-for-agency.pickle'), "rb") as pickle_file:
            response = pickle.load(pickle_file)
        print("Route URLs loaded from pickle cache.")
    finally:
        routes = response.json()
        print('Found {} routes. Fetching current positions with ASYNCHRONOUS requests...'.format(len(routes['data']['list'])))

    for route in routes['data']['list']:
        path_list.append({route['id']:"/api/siri/vehicle-monitoring.json?key={}&VehicleMonitoringDetailLevel=calls&LineRef={}".format(os.getenv("API_KEY"), route['id'])})

    return path_list

# def dump_to_screen(feeds):
#     for route_bundle in feeds:
#         for route_id, data in route_bundle.items():
#             print (data.json())
#     return

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
    timestamp = datetime.now()
    timestamp_pretty = timestamp.strftime("%Y-%m-%dT_%H:%M:%S.%f")
    for route_bundle in feeds:
        for route_id,route_report in route_bundle.items():
            dumpfile=(filepath() + route_id.split()[1] + '_' + timestamp_pretty +'.gz')
            with gzip.open(dumpfile, 'wt', encoding="ascii") as zipfile:
                try:
                    json.dump(route_report.json(), zipfile)
                except:
                    raise Exception
    return timestamp

def dump_to_db(dbparams,timestamp, feeds):

    session,db_url = db.get_session(dbparams)
    print('Dumping to {}'.format(db_url))
    num_buses = 0
    for route_bundle in feeds:
        for route_id,route_report in route_bundle.items():
            buses = db.parse_buses(timestamp, route_id, route_report.json(), db_url)
            for bus in buses:
                session.add(bus)
                num_buses = num_buses + 1 # bug not working
        session.commit()
    return num_buses




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
    num_buses = dump_to_db(dbparams,timestamp, feeds)  # bug broke?

    end = time.time()
    print('\nFetched {} buses on {} routes in {:2f} seconds to uncompressed archive and database.'.format(num_buses,len(feeds),(end - start)))

