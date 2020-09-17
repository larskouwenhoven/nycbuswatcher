
from urllib.request import urlopen
import argparse

import os
import json
import datetime


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Database import BusObservation

# load API KEY from .env (dont commit this file to the repo)
from dotenv import load_dotenv
load_dotenv()

# database settings
MYSQL_DB='buses'
MSQL_HOST='127.0.0.1'
MYSQL_USER='nycbuswatcher'
MYSQL_PASSWORD='bustime'



def get_feed(route, output):

    # fetch and prep feed
    # API reference http://bustime.mta.info/wiki/Developers/SIRIVehicleMonitoring

    if route == "ALL":
        url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=" + os.getenv(
            "API_KEY") + "&VehicleMonitoringDetailLevel=calls"
        response = urlopen(url, timeout=120)
        data = response.read().decode("utf-8")
        data = json.loads(data)

    else:
        url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=" + os.getenv("API_KEY") + "&VehicleMonitoringDetailLevel=calls&LineRef=" + route
        response = urlopen(url)
        data = response.read().decode("utf-8")
        data = json.loads(data)

    if output == 'screen':
        dump_to_screen(data,route)
    elif output == 'file':
        dump_to_file(data, route)
    elif output in ['sqlite','mysql']:
        dump_to_db(data, route, output)

    return data



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
    date = datetime.datetime.now().strftime("%Y-%m-%dT_%H:%M:%S.%f")
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

def get_session(output):
    db_url=get_db_url(output)
    engine = create_engine(db_url, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session,db_url

def get_db_url(output):
    if output == 'mysql':
        db_url = 'mysql://{}:{}@{}/{}'.format(MYSQL_USER,MYSQL_PASSWORD,MSQL_HOST,MYSQL_DB)
    elif output == 'sqlite':
        db_url='sqlite:///data/buses.db'
    return db_url


def parse_buses(route,data,db_url):

    # lookup maps my databsae columns to a tuple of terms used to crawl the json
    # below ['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']
    # per http://bustime.mta.info/wiki/Developers/SIRIMonitoredVehicleJourney

    # todo all MonitoredCall substructure, e.g. next stop

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

    for b in data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']:

        bus = BusObservation(route,db_url)

        for k,v in lookup.items():
            try:
                if len(v) > 1:
                    val = b['MonitoredVehicleJourney'][v[0]][v[1]]
                    setattr(bus, k, val)
                    print(k,val)
                else:
                    val = b['MonitoredVehicleJourney'][v[0]]
                    setattr(bus, k, val)
                    print(k, val)
            except LookupError:
                pass
            except Exception as e:
                print (e)
                pass


        # result = ("{}\t{}\t{}\t{}").format(route,bus.vehicle_id,bus.trip_id,bus.progress_rate,bus.destination_name,bus.lat,bus.lon)
        # print(result)

        buses.append(bus)

    return buses # return a list of BusObservation objects




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='NYCbuswatcher grabber, fetches and stores current position for buses')
    parser.add_argument('-r', action="store", dest="route") # a single route M1 or ALL
    parser.add_argument('-o', action="store", dest="output", default="screen") # output file, sqlite, mysql, screen
    parser.add_argument('-p', action="store_true", dest="production")  # output file, db, screen # todo makes it loop? or should that be done externally?
    args = parser.parse_args()

    if args.production is True:
        route = 'ALL'
        output = 'mysql'
    else:
        route=args.route
        output=args.output


    data = get_feed(route, output)

    print ('grabber found {} buses on route(s) {}.'.format(len(data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']),args.route))




