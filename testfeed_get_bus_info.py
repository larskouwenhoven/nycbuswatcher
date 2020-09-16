
from __future__ import print_function
import json
from urllib.request import urlopen
import sys

# load API KEY from .env (dont commit this file to the repo)
import os
from dotenv import load_dotenv
load_dotenv()


if not len(sys.argv) == 3:
    print("Invalid number of arguments. Run as: python  testfeed_get_bus_info.py <BUS_LINE> <BUS_LINE>.csv")
    sys.exit()

# Defining URL to obtain the information from MTA API
url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=" + os.getenv("API_KEY")  + "&VehicleMonitoringDetailLevel=calls&LineRef=" + sys.argv[1]

response = urlopen(url)
#Reading the response from the Site and Decoding it to UTF-8 Format
data = response.read().decode("utf-8")
#Converting the File to JSON Format
data = json.loads(data)

# dump the data to a file
with open('testfeed_bus_info.json', 'w') as outfile:
    json.dump(data, outfile)


#This variable stores the value of the No. of Buses by 

No_buses = len(data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'])

#Opening the CSV File in Write Mode and writing the details from JSON 

fout = open(sys.argv[2], "w")
fout.write("Latitude,Longitude,Stop Name,Stop Status\n")

for n in (range(0, No_buses)):

    bus_lat = data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][n]['MonitoredVehicleJourney']['VehicleLocation']['Latitude']
    bus_lon = data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][n]['MonitoredVehicleJourney']['VehicleLocation']['Longitude']
    try: 
      bus_stop = data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][n]['MonitoredVehicleJourney']['OnwardCalls']['OnwardCall'][0]['StopPointName']
    except LookupError:
      bus_stop = "N/A"
     
    try:
      bus_status = data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][n]['MonitoredVehicleJourney']['OnwardCalls']['OnwardCall'][0]['Extensions']['Distances']['PresentableDistance']
    except LookupError:
      bus_status = "N/A"

    fout.write("%s,%s,%s,%s\n" %(bus_lat, bus_lon, bus_stop, bus_status))

fout.close()

