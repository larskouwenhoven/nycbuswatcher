import os
import json
from urllib.request import urlopen
import argparse

import Database as db


# load API KEY from .env (dont commit this file to the repo)
from dotenv import load_dotenv
load_dotenv()


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

    if args.output == 'screen':
        db.dump_to_screen(data,route)
    elif args.output == 'file':
        db.dump_to_file(data, route)
    elif args.output == 'db':
        db.dump_to_db(data, route)


    return data



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='NYCbuswatcher grabber, fetches and stores current position for buses')
    parser.add_argument('-r', action="store", dest="route") # a single route M1 or ALL
    parser.add_argument('-o', action="store", dest="output") # output file, db, screen
    # parser.add_argument('-p', action="store_true", dest="production")  # output file, db, screen # todo add production flag that defaults to -r ALL and -o file, db
    args = parser.parse_args()

    data = get_feed(args.route, args.output)
    num_buses = len(data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'])
    print ('grabber found {} buses on route(s) {}.'.format(num_buses,args.route))




