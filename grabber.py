import os
import json
from urllib.request import urlopen
import argparse

import Database as db


# load API KEY from .env (dont commit this file to the repo)
from dotenv import load_dotenv
load_dotenv()


def get_feed(route):
    # fetch and prep feed
    # API reference http://bustime.mta.info/wiki/Developers/SIRIVehicleMonitoring

    if route == "ALL":
        url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=" + os.getenv(
            "API_KEY") + "&VehicleMonitoringDetailLevel=calls"
        response = urlopen(url) # bug increase response timeout when route=ALL?
        data = response.read().decode("utf-8")
        data = json.loads(data)

    else:
        url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=" + os.getenv("API_KEY") + "&VehicleMonitoringDetailLevel=calls&LineRef=" + route
        response = urlopen(url)
        data = response.read().decode("utf-8")
        data = json.loads(data)

    if args.debug == True:
        db.dump_to_screen(data,route)
    db.dump_to_json(data, route)
    db.dump_to_table(data,route) #todo call ps.parse_buses

    return data



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='NYCbuswatcher grabber, fetches and stores current position for buses')
    parser.add_argument('-r', action="store", dest="route") # a single route M1 or ALL
    parser.add_argument('-d', action="store_true", dest="debug")
    args = parser.parse_args()

    data = get_feed(args.route)
    num_buses = len(data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'])
    print ('grabber found {} on route(s) {}.'.format(num_buses,args.route))




