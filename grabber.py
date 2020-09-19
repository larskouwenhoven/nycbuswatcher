
# from urllib.request import urlopen
import argparse
from datetime import datetime
import time
import os
import json
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

from Database import BusObservation

# load API KEY from .env (dont commit this file to the repo)
load_dotenv()


def get_feed(route, output,interval):
    # fetch and prep feed
    # API reference http://bustime.mta.info/wiki/Developers/SIRIVehicleMonitoring

    # if route == "ALL":
    #     url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=" + os.getenv(
    #         "API_KEY") + "&VehicleMonitoringDetailLevel=calls"
    #
    #     try:
    #         response = requests.get(url, timeout=interval)
    #         data = response.json()
    #         # response = urlopen(url, timeout=120)
    #         # data = response.read().decode("utf-8")
    #         # data = json.loads(data)
    #     except ConnectionError:
    #         return #soon right directive?
    #
    #

    if route == "ALL":
        routelist = get_routelist()
        data = []
        for route in routelist:

            url = ("http://bustime.mta.info/api/siri/vehicle-monitoring.json?key={}&VehicleMonitoringDetailLevel=calls&LineRef={}").format(os.getenv(
                "API_KEY"),route)

            try:
                response = requests.get(url, timeout=interval)
                bus_json = response.json()
                # response = urlopen(url, timeout=120)
                # data = response.read().decode("utf-8")
                # data = json.loads(data)
            except ConnectionError:
                return  # soon right directive?
        data.append(bus_json) #todo this will be a list of JSON dicts, so might need to parse differently

    else:
        try:

            url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=" + os.getenv("API_KEY") + "&VehicleMonitoringDetailLevel=calls&LineRef=" + route
            response = requests.get(url, timeout=30)
            data = response.json()

        except ConnectionError:
            return #soon right directive?


    if output == 'screen':
        dump_to_screen(data,route)
    elif output == 'file':
        dump_to_file(data, route)
    elif output in ['sqlite','mysql']:
        dump_to_db(data, route, output)

    # todo log response.elapsed somewhere to throttle the interval for future jobs (touch a file somewhere with a running average and most recent time?)

    return

def get_routelist():
    url = "http://bustime.mta.info/api/where/routes-for-agency/MTA%20NYCT.json?key=" + os.getenv("API_KEY")
    response = requests.get(url, timeout=30)
    routes = response.json()

    pp=pprint.PrettyPrinter(indent=4)

    pp.pprint (routes)

    routelist=[]

    for route in routes['data']['list']:
        # routelist.append(route['shortName'])
        routelist.append(route['id'])

    return routelist

def dump_to_screen(data,route):
    print(json.dumps(data, indent=2))
    return


def dump_to_file(data, route):
    path = ("data/")
    check = os.path.isdir(path)
    if not check:
        os.makedirs(path)
        print("created folder : ", path)
    else:
        # print(path, "folder already exists.")
        pass
    date = datetime.now().strftime("%Y-%m-%dT_%H:%M:%S.%f")
    dumpfile=(path + route + '_' + date +'.json')
    with open(dumpfile, 'w') as json_file:
        json.dump(data, json_file)
    return


def dump_to_db(data, route, output):
    session,db_url = get_session(output)
    for bus in parse_buses(route, data,db_url):
        session.add(bus)
    session.commit()
    return

def get_session(output,):
    db_url=get_db_url(output)
    engine = create_engine(db_url, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session,db_url

def get_db_url(output):
    if output == 'mysql':
        db_url = 'mysql://{}:{}@{}/{}'.format(dbparams['dbuser'],dbparams['dbpassword'],'mysql_docker',dbparams['dbname']) # todo VIP test if production or not
    elif output == 'sqlite':
        db_url='sqlite:///data/buses.db'
    return db_url


def parse_buses(route,data,db_url):

    # lookup maps my databsae columns to a tuple of terms used to crawl the json
    # below ['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']
    # per http://bustime.mta.info/wiki/Developers/SIRIMonitoredVehicleJourney

    # future all MonitoredCall substructure, e.g. next stop

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



    #todo VIP if routes="ALL" will need to loop over below? or are we only getting called once per feed fetch already?
    #todo might make sense to make that all more linear
    #todo so the fetch, parse, and dump happens for each route in one function, or group of functions
    #todo and if we need to do it for ALL routes, we are looping over a list built by a call to get_routelist


    for b in data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']:

        bus = BusObservation(route,db_url,datetime.now())

        for k,v in lookup.items():
            try:
                if len(v) > 1:
                    val = b['MonitoredVehicleJourney'][v[0]][v[1]]
                    setattr(bus, k, val)
                    # print(k,val)
                else:
                    val = b['MonitoredVehicleJourney'][v[0]]
                    setattr(bus, k, val)
                    # print(k, val)
            except LookupError:
                pass
            except Exception as e:
                print (e)
                pass

        buses.append(bus)

    return buses



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='NYCbuswatcher grabber, fetches and stores current position for buses')
    parser.add_argument('-r', action="store", dest="route") # a single route M1 or ALL
    parser.add_argument('-o', action="store", dest="output", default="screen") # screen, file, sqlite, mysql
    parser.add_argument('-p', action="store_true", dest="production")
    args = parser.parse_args()

    # database settings

    dbparams={
        'dbname':'buses',
        'dbuser':'nycbuswatcher',
        'dbpassword':'bustime'
    }


    if args.production is True:
        route = 'ALL'
        # route = 'M1'
        output = 'mysql'

    else:
        route=args.route
        output=args.output

    interval = 60
    if route == 'ALL':
        interval = 180 #todo read this from the dynamically calculated time?


    scheduler = BackgroundScheduler()
    scheduler.add_job(get_feed, 'interval', seconds=interval,args=[route, output,interval])
    scheduler.start()
    print('Scanning on {}-second interval. Press Ctrl+{} to exit'.format(interval,('Break' if os.name == 'nt' else 'C')))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()



