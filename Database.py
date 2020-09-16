import os
import json
import datetime

# from sqlalchemy import *
from sqlalchemy import Column, Date, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class BusObservation(Base):
    __tablename__ = "buses"
    id = Column(Integer, primary_key=True)
    route_simple=Column(String) #this is the route name passed through from the command line, may or may not match route_short
    route_long=Column(String)
    direction=Column(String)
    service_date=Column(String)
    trip_id=Column(String)
    gtfs_shape_id=Column(String)
    route_short=Column(String)
    agency=Column(String)
    origin_id=Column(String)
    destination_id=Column(String)
    destination_name=Column(String)
    scheduled_origin=Column(String)
    alert=Column(String)
    lat=Column(Float)
    lon=Column(Float)
    bearing=Column(Float)
    progress_rate=Column(String)
    progress_status=Column(String)
    occupancy=Column(String)
    vehicle_id=Column(String)
    gtfs_block_id=Column(String)

    # def __repr__(self):# todo repr
    #    return (f'{self.__class__.__name__}('
    #            f'{self.color!r}, {self.mileage!r})')

    def __init__(self, route):
        self.route_simple = route

engine = create_engine('sqlite:///data/buses.db', echo=True)
Base.metadata.create_all(engine)


def get_session(route):
    engine = create_engine('sqlite:///data/buses.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def dump_to_table(data, route):
    session=get_session(route)
    session.add(parse_buses(route, data))
    session.commit()
    return

def dump_to_json(data, route):
    path = ("data/")
    check = os.path.isdir(path)
    if not check:
        os.makedirs(path)
        print("created folder : ", path)
    else:
        print(path, "folder already exists.")
    date = datetime.datetime.now().strftime("%Y-%m-%dT_%H:%M:%S.%f")
    dumpfile=(path + route + '_' + date +'.json')
    with open(dumpfile, 'w') as json_file:
        json.dump(data, json_file)
    return

def dump_to_screen(data,route):
    print(json.dumps(data, indent=2))
    return



def parse_buses(route,data):

    # reference to crawl the json response
    # below ['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']
    # per http://bustime.mta.info/wiki/Developers/SIRIMonitoredVehicleJourney

    lookup = {'route_long':'LineRef',
              'direction':'DirectionRef',
              'service_date': ('FramedVehicleJourneyRef', 'DataFrameRef'),
              'trip_id': ('FramedVehicleJourneyRef', 'DatedVehicleJourneyRef'),
              'gtfs_shape_id': 'JourneyPatternRef',
              'route_short': 'PublishedLineName',
              'agency': 'OperatorRef',
              'origin_id':'OriginRef',
              'destination_id':'DestinationRef',
              'destination_name':'DestinationName',
              'scheduled_origin':'OriginAimedDepartureTime',
              # 'alert': ('SituationRef', 'SituationSimpleRef'), #todo optional
              'lat':('VehicleLocation','Latitude'),
              'lon':('VehicleLocation','Longitude'),
              'bearing': 'Bearing',
              'progress_rate': 'ProgressRate',
              # 'progress_status': 'ProgressStatus', #todo optional
              # 'occupancy': 'Occupancy', #todo optional
              'vehicle_id':'VehicleRef',
              'gtfs_block_id':'BlockRef'
              #todo all MonitoredCall, e.g. next stop
              }

    # num_buses = len(data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'])

    buses = []

    for b in data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']:

        bus = BusObservation(route)

        for k,v in lookup.items():
            try:
                if len(v) > 1:
                    bus.k = b['MonitoredVehicleJourney'][v[0]][v[1]]
                else:
                    bus.k = b['MonitoredVehicleJourney'][v]
            except LookupError:
                continue # field not present. restart the loop. change to pass if code follows in this for loop

        result = ("{}\t{}\t{}\t{}").format(route,bus.vehicle_id,bus.trip_id,bus.progress_rate,bus.destination_name,bus.lat,bus.lon)
        print(result)

        buses.append(bus)

    return buses # return a list of BusObservation objects

