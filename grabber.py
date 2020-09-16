import os, sys
import json
from urllib.request import urlopen
import argparse
import untangle

# load API KEY from .env (dont commit this file to the repo)
from dotenv import load_dotenv
load_dotenv()


def get_feed(route):
    # fetch and prep feed
    url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=" + os.getenv(
        "API_KEY") + "&VehicleMonitoringDetailLevel=calls&LineRef=" + args.route
    response = urlopen(url)
    data = response.read().decode("utf-8")
    data = json.loads(data)

    # This variable stores the value of the No. of Buses by
    num_buses = len(data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'])

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

        result = ("%s,%s,%s,%s\n" % (bus_lat, bus_lon, bus_stop, bus_status))
        print(result)
        return result


# command line parser
parser = argparse.ArgumentParser(description='NYCbuswatcher grabber, fetches and stores current position for buses')
parser.add_argument('-r', action="store", dest="route") # a single route or 'ALL'
args = parser.parse_args()


# if all, get list of routes
if args.route == "ALL":
    print ('not fully implemented, single route only for now')
    url = "http://bustime.mta.info/api/where/routes-for-agency/MTA%20NYCT.xml?"+os.getenv("API_KEY") # bug the space %20 is breaking this. not sure how to escape it
    print(url)
    data=untangle.parse(url)
    routes = []
    print (routes)
    # todo unpack this to get a list of routes to pass into get_feed()
else:
    routes = args.route

for r in routes:
    get_feed(r)


