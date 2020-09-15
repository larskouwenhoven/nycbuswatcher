# Program to track each vehicle of a particular line
from __future__ import print_function
import pylab as pl
import json
import urllib
import sys



if not len(sys.argv) == 3:
    print("The Program has not been executed - Invalid number of arguments. Run as: python show_bus_locations.py <MTA_KEY> <BUS_LINE>")
    sys.exit()

# Defining URL to obtain the information from MTA API
url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=" + sys.argv[1]  + "&VehicleMonitoringDetailLevel=calls&LineRef=" + sys.argv[2]
response = urllib.urlopen(url)
#Reading the response from the Site and Decoding it to UTF-8 Format
data = response.read().decode("utf-8")
#Converting the File to JSON Format
data = json.loads(data)
#This variable stores the value of the No. of Buses by 

No_buses = len(data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'])


print ("Bus Line:" + sys.argv[2])

print ("No. of Buses that are currently Active:%s"%(No_buses))

#A for loop that prints the location of each bus and runs until the count of the buses
for n in range(No_buses):
     Bus_lat = data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][n]['MonitoredVehicleJourney']['VehicleLocation']['Latitude']
     Bus_lon = data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][n]['MonitoredVehicleJourney']['VehicleLocation']['Longitude']
     print ("The Bus %s is at Latitude  %s and Longitude %s" %(n+1, Bus_lat, Bus_lon))
