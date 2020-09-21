# https://asks.readthedocs.io/en/latest/
# many_get.py
# make a whole pile of api calls and store
# their response objects in a list.
# Using the homogeneous-session.

import os

import asks
import curio

from dotenv import load_dotenv
load_dotenv()



from datetime import datetime
import time

import sys
import json

import requests

def get_path_list():
    path_list=[]
    routelist = get_routelist()
    for route in routelist:
        routepath = ("/api/siri/vehicle-monitoring.json?key={}&VehicleMonitoringDetailLevel=calls&LineRef={}").format(os.getenv("API_KEY"),route)
    path_list.append(routepath)
    return path_list

def get_routelist():
    url = "http://bustime.mta.info/api/where/routes-for-agency/MTA%20NYCT.json?key=" + os.getenv("API_KEY")
    response = requests.get(url, timeout=30)
    routes = response.json()
    print('Found {} routes. Fetching current positions...'.format(len(routes['data']['list'])))
    routelist=[]
    for route in routes['data']['list']:
        routelist.append(route['id'])
    return routelist

async def grabber(route, s):
    r = await s.get(route=route)
    retrieved_responses.append(r)

async def main(s):
    routelist = get_routelist()
    for route in routelist:
        curio.spawn(grabber(route, s))


#
# def get_buses():
#     start = time.time()
#     routelist = get_routelist()
#     data = []
#     for route in routelist:
#         url = ("
#         try:
#             # sys.stdout.write('>')
#             response = requests.get(url, timeout=30)
#             bus_json = response.json()
#             # raise ConnectionError
#         except ConnectionError:
#             return  # right directive to handle this?
#         data.append({route:bus_json})
#     end = time.time()
#     print('\nFetched {} routes in {} seconds, dumping to compressed archive and database.'.format(len(routelist),(end - start)))
#     return
#
#
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

    path_list=get_path_list()
    s = asks.Session('http://bustime.mta.info', connections=20)
    retrieved_responses = []

    curio.run(main(s))
    parse_buses(retrieved_responses)



