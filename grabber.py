from datetime import datetime
import time
import os
import sys
import json

import argparse
import requests
import gzip

from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

import Database as db


# load API KEY from .env (dont commit this file to the repo)
load_dotenv()


def get_buses(dbparams):
    start = time.time()
    routelist = get_routelist()
    data = []
    for route in routelist:
        url = ("http://bustime.mta.info/api/siri/vehicle-monitoring.json?key={}&VehicleMonitoringDetailLevel=calls&LineRef={}").format(os.getenv("API_KEY"),route)
        try:
            # sys.stdout.write('>')
            response = requests.get(url, timeout=30)
            bus_json = response.json()
            # raise ConnectionError
        except ConnectionError:
            return  # right directive to handle this?
        data.append({route:bus_json})
    end = time.time()
    print('\nFetched {} routes in {} seconds, dumping to compressed archive and database.'.format(len(routelist),(end - start)))
    # dump_to_file(data) # for backup
    # dump_to_db(data,dbparams)
    return


def get_routelist():
    url = "http://bustime.mta.info/api/where/routes-for-agency/MTA%20NYCT.json?key=" + os.getenv("API_KEY")
    response = requests.get(url, timeout=30)
    routes = response.json()
    print('Found {} routes. Fetching current positions...'.format(len(routes['data']['list'])))
    routelist=[]
    for route in routes['data']['list']:
        routelist.append(route['id'])
    return routelist


def dump_to_file(data):
    path = ("data/")
    check = os.path.isdir(path)
    if not check:
        os.makedirs(path)
        print("created folder : ", path)
    else:
        pass
    date = datetime.now().strftime("%Y-%m-%dT_%H:%M:%S.%f")
    for route_bundle in data:
        for route_id,route_report in route_bundle.items():
            dumpfile=(path + route_id.split()[1] + '_' + date +'.gz')
            # with open(dumpfile, 'w') as json_file:
            #    json.dump(data, json_file)
            #
            # from https://stackoverflow.com/questions/49534901/is-there-a-way-to-use-json-dump-with-gzip/49535758#49535758
            with gzip.open(dumpfile, 'wt', encoding="ascii") as zipfile:
                json.dump(route_report, zipfile)
    return


def dump_to_db(data,dbparams):
    session,db_url = db.get_session(dbparams)
    print('Dumping to {}'.format(db_url))
    for route_bundle in data:
        sys.stdout.write(' <{}> '.format(str(next(iter(route_bundle)))))
        for route_id,route_report in route_bundle.items():
            for bus in parse_buses(route_id, route_report, db_url):
                session.add(bus)
        session.commit()
    return


def parse_buses(route,data,db_url):
    lookup = {'route_long':['LineRef'],
              'direction':['DirectionRef'],
              'service_date': ['FramedVehicleJourneyRef', 'DataFrameRef'],
              'trip_id': ['FramedVehicleJourneyRef', 'DatedVehicleJourneyRef'],
              'gtfs_shape_id': ['JourneyPatternRef'],
              'route_short': ['PublishedLineName'],
              'agency': ['OperatorRef'],
              'origin_id':['OriginRef'],
              'destination_id':['DestinationRef'],
              'destination_name':['DestinationName'],
              # 'scheduled_origin':['OriginAimedDepartureTime'], # appears to be omitted from feed
              'alert': ['SituationRef', 'SituationSimpleRef'],
              'lat':['VehicleLocation','Latitude'],
              'lon':['VehicleLocation','Longitude'],
              'bearing': ['Bearing'],
              'progress_rate': ['ProgressRate'],
              'progress_status': ['ProgressStatus'],
              'occupancy': ['Occupancy'],
              'vehicle_id':['VehicleRef'],
              'gtfs_block_id':['BlockRef']
              }
    buses = []
    try:
        for b in data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']:
            bus = db.BusObservation(route,db_url,datetime.now())
            for k,v in lookup.items():
                try:
                    if len(v) > 1:
                        val = b['MonitoredVehicleJourney'][v[0]][v[1]]
                        setattr(bus, k, val)
                    else:
                        val = b['MonitoredVehicleJourney'][v[0]]
                        setattr(bus, k, val)
                except LookupError:
                    pass
                except Exception as e:
                    print (e)
                    pass
            sys.stdout.write('.')
            buses.append(bus)
    except KeyError: #no VehicleActivity?
        pass
    return buses


if __name__ == "__main__":

    dbparams = {
        'dbname': 'buses',
        'dbuser': 'nycbuswatcher',
        'dbpassword': 'bustime'
    }

    parser = argparse.ArgumentParser(description='NYCbuswatcher grabber, fetches and stores current position for buses')
    parser.add_argument('-p', action="store_true", dest="production")
    args = parser.parse_args()

    if args.production is True:

        interval = 180
        dbparams['dbhost']='mysql_docker'
        print('NYC MTA BusTime API Scraper v0.1. Anthony Townsend <atownsend@cornell.edu>')
        print('Scanning on {}-second interval.'.format(interval))
        scheduler = BackgroundScheduler()
        scheduler.add_job(get_buses, 'interval', seconds=interval,args=[dbparams])
        scheduler.start()
        try:
            while True:
                time.sleep(2)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()

    elif args.production is False: #run once and quit
        dbparams['dbhost']='localhost'
        get_buses(dbparams)