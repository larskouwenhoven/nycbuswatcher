



def parse_buses(data):


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

        result = ("%s\t%s\t%s %s" % (bus_lat, bus_lon, bus_status, bus_stop, ))
        print(result)

    return result