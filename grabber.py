import argparse
import requests
import os
from datetime import datetime
import json
import time
import gzip
import pickle

from apscheduler.schedulers.background import BackgroundScheduler
import trio
from dotenv import load_dotenv

import Database as db
# from grabroutemaps import GTFS2GeoJSON
from config import config


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
        print('Found {} routes.'.format(len(routes['data']['list'])))

    for route in routes['data']['list']:
        path_list.append({route['id']:"/api/siri/vehicle-monitoring.json?key={}&VehicleMonitoringDetailLevel=calls&LineRef={}".format(os.getenv("API_KEY"), route['id'])})

    return path_list


def filepath():
    path = ("data/")
    check = os.path.isdir(path)
    if not check:
        os.makedirs(path)
        print("created folder : ", path)
    else:
        pass
    return path


def get_db_args():

    if args.localhost is True: #n.b. this ignores what's in config/development.py
        dbhost = 'localhost'
    elif os.environ['PYTHON_ENV'] == "development":
        dbhost = 'localhost'
    else:
        dbhost = config.config['dbhost']

    return (config.config['dbuser'],
            config.config['dbpassword'],
            dbhost,
            config.config['dbname']
            )

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
                    pass # if error, dont write and return
    return timestamp


def dump_to_db(timestamp, feeds):
    db_url=db.get_db_url(*get_db_args())
    db.create_table(db_url)
    session = db.get_session(*get_db_args())
    print('Dumping to {}'.format(db_url))
    num_buses = 0
    for route_bundle in feeds:
        for route_id,route_report in route_bundle.items():
            buses = db.parse_buses(timestamp, route_id, route_report.json(), db_url)
            for bus in buses:
                session.add(bus)
                num_buses = num_buses + 1
        session.commit()
    return num_buses


def async_grab_and_store():

    start = time.time()
    path_list = get_path_list()
    feeds = []

    async def grabber(s,a_path,route_id):
        try:
            r = await s.get(path=a_path) # bug need to trap connection errors here
        except ValueError as e :
            print ('{} from DNS issues'.format(e))
        feeds.append({route_id:r})

    async def main(path_list):
        from asks.sessions import Session
        s = Session('http://bustime.mta.info', connections=config.config['http_connections'])
        async with trio.open_nursery() as n:
            for path_bundle in path_list:
                for route_id,path in path_bundle.items():
                    n.start_soon(grabber, s, path, route_id )

    trio.run(main, path_list)

    timestamp = dump_to_file(feeds)
    num_buses = dump_to_db(timestamp, feeds)
    end = time.time()
    print('Fetched {} buses on {} routes in {:2f} seconds to gzipped archive and mysql database.\n'.format(num_buses,len(feeds),(end - start)))

    return



if __name__ == "__main__":

    print('NYC MTA BusTime API Scraper v1.0. October 2020. Anthony Townsend <atownsend@cornell.edu>')
    print('mode: {}'.format(os.environ['PYTHON_ENV']))

    parser = argparse.ArgumentParser(description='NYCbuswatcher grabber, fetches and stores current position for buses')
    parser.add_argument('-l', action="store_true", dest="localhost", help="force localhost for production mode")
    args = parser.parse_args()

    load_dotenv()

    # PRODUCTION = start main loop
    if os.environ['PYTHON_ENV'] == "production":
        interval = 60
        print('Scanning on {}-second interval.'.format(interval))
        scheduler = BackgroundScheduler()
        scheduler.add_job(async_grab_and_store, 'interval', seconds=interval)
        # scheduler.add_job(GTFS2GeoJSON.update_route_map(), hours=24) #todo reinstall pandas and shapely to conda and add this back
        scheduler.start()
        try:
            while True:
                time.sleep(2)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()

    # DEVELOPMENT = run once and quit
    elif os.environ['PYTHON_ENV'] == "development":
        async_grab_and_store()



