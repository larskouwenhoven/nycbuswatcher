import os, sys
import json
from urllib.request import urlopen
import argparse

from Database import dump_api_response

# load API KEY from .env (dont commit this file to the repo)
from dotenv import load_dotenv
load_dotenv()


def get_feed(route):
    # fetch and prep feed
    # API reference http://bustime.mta.info/wiki/Developers/SIRIVehicleMonitoring

    if args.route == "ALL":
        url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=" + os.getenv(
            "API_KEY") + "&VehicleMonitoringDetailLevel=calls"
        response = urlopen(url)
        data = response.read().decode("utf-8")
        data = json.loads(data)
    else:
        url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=" + os.getenv(
            "API_KEY") + "&VehicleMonitoringDetailLevel=calls&LineRef=" + args.route
        response = urlopen(url)
        data = response.read().decode("utf-8")
        data = json.loads(data)
    dump_api_response(data,route)
    return data



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='NYCbuswatcher grabber, fetches and stores current position for buses')
    parser.add_argument('-r', action="store", dest="route") # a single route M1 or ALL
    args = parser.parse_args()

    data = get_feed(args.route)
    num_buses = len(data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'])
    print ('grabber found {} on route(s) {}.'.format(num_buses,args.route))

    for n in (range(0, num_buses)):

        bus_lat = \
            data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][n][
                'MonitoredVehicleJourney'][
                'VehicleLocation']['Latitude']
        bus_lon = \
            data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][n][
                'MonitoredVehicleJourney'][
                'VehicleLocation']['Longitude']

        try:
            bus_stop = data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][n][
                'MonitoredVehicleJourney']['OnwardCalls']['OnwardCall'][0]['StopPointName']
        except LookupError:
            bus_stop = "N/A"

        try:
            bus_status = data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][n][
                'MonitoredVehicleJourney']['OnwardCalls']['OnwardCall'][0]['Extensions']['Distances'][
                'PresentableDistance']
        except LookupError:
            bus_status = "N/A"

        result = ("%s\t%s\t%s %s" % (bus_lat, bus_lon, bus_status, bus_stop, ))
        print(result)
