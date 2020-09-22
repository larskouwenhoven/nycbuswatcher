# many_get.py
# make a whole pile of api calls and store
# their response objects in a list.
# Using the homogeneous-session.
import requests
import os
from datetime import datetime
import json
import time
import gzip

import Database as db

from dotenv import load_dotenv
load_dotenv()

import trio


def get_path_list():
    path_list = []
    url = "http://bustime.mta.info/api/where/routes-for-agency/MTA%20NYCT.json?key=" + os.getenv("API_KEY")
    response = requests.get(url, timeout=30)
    routes = response.json()
    print('Found {} routes. Fetching current positions with ASYNCHRONOUS requests...'.format(len(routes['data']['list'])))
    for route in routes['data']['list']:
        path_list.append({route['id']:"/api/siri/vehicle-monitoring.json?key={}&VehicleMonitoringDetailLevel=calls&LineRef={}".format(os.getenv("API_KEY"), route['id'])})
    return path_list

def dump_to_screen(feeds):
    for route_bundle in feeds:
        for route_id, data in route_bundle.items():
            print (data.json())
    return

def dump_to_file(feeds):
    path = ("data/")
    check = os.path.isdir(path)
    if not check:
        os.makedirs(path)
        print("created folder : ", path)
    else:
        pass
    timestamp = datetime.now()
    timestamp_pretty = timestamp.strftime("%Y-%m-%dT_%H:%M:%S.%f")
    for route_bundle in feeds:
        for route_id,route_report in route_bundle.items():

            # # uncompressed version
            # dumpfile=(path + route_id.split()[1] + '_' + timestamp_pretty +'.json')
            # with open(dumpfile, 'w') as json_file:
            #    json.dump(route_report.json(), json_file, indent=4)

            # compressed
            dumpfile=(path + route_id.split()[1] + '_' + timestamp_pretty +'.gz')
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

    # # todo add production switch + chane dbhost to 'mysql_docker'
    # parser = argparse.ArgumentParser(description='NYCbuswatcher grabber, fetches and stores current position for buses')
    # parser.add_argument('-p', action="store_true", dest="production")
    # args = parser.parse_args()


    # # todo add scheduler
    # from apscheduler.schedulers.background import BackgroundScheduler
    # from dotenv import load_dotenv
    # if args.production is True:
    #
    #     interval = 180
    #     dbparams['dbhost']='mysql_docker'
    #     print('NYC MTA BusTime API Scraper v0.1. Anthony Townsend <atownsend@cornell.edu>')
    #     print('Scanning on {}-second interval.'.format(interval))
    #     scheduler = BackgroundScheduler()
    #     scheduler.add_job(get_buses, 'interval', seconds=interval,args=[dbparams])
    #     scheduler.start()
    #     try:
    #         while True:
    #             time.sleep(2)
    #     except (KeyboardInterrupt, SystemExit):
    #         scheduler.shutdown()
    #
    # elif args.production is False: #run once and quit
    #     dbparams['dbhost']='localhost'
    #     get_buses(dbparams)



    dbparams = {
        'dbname': 'buses',
        'dbuser': 'nycbuswatcher',
        'dbpassword': 'bustime',
        'dbhost':'localhost'
    }

    path_list = get_path_list()

    feeds = []

    async def grabber(s,a_path,route_id):
        r = await s.get(path=a_path)
        feeds.append({route_id:r})

    async def main(path_list):
        from asks.sessions import Session
        s = Session('http://bustime.mta.info', connections=5) # todo move this to a parameter. low for development to avoid DNS errors, higher OK in production
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



