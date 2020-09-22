from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Date, DateTime, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base


def get_session(dbparams):
    db_url = 'mysql://{}:{}@{}/{}'.format(dbparams['dbuser'],dbparams['dbpassword'],dbparams['dbhost'],dbparams['dbname'])
    engine = create_engine(db_url, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session,db_url

def parse_buses(timestamp, route, data, db_url): #todo this is slower than expected (~0.25 seconds per route)
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
    try: #bug 'list indices must be integers or strings — BY STEPPING THROUGH THIS SECTION UNTIL IT APPEARS IN CONSOLE
        for b in data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']:
            bus = BusObservation(route,db_url,timestamp)
            for k,v in lookup.items(): #todo speed this up by reversing the key:value pairs in lookup, and simply using b here as the key and getting the value from lookup
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
            # print(bus)
            buses.append(bus)
    except KeyError: #no VehicleActivity?
        pass
    return buses




Base = declarative_base()

class BusObservation(Base): #future optimize STRING field lengths
    __tablename__ = "buses"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    route_simple=Column(String(255)) #this is the route name passed through from the command line, may or may not match route_short
    route_long=Column(String(255))
    direction=Column(String(255))
    service_date=Column(String(255)) #future check inputs and convert to Date
    trip_id=Column(String(255))
    gtfs_shape_id=Column(String(255))
    route_short=Column(String(255))
    agency=Column(String(255))
    origin_id=Column(String(255))
    destination_id=Column(String(255))
    destination_name=Column(String(255))
    # scheduled_origin=Column(String) # appears to be omitted from feed
    alert=Column(String(255))
    lat=Column(Float)
    lon=Column(Float)
    bearing=Column(Float)
    progress_rate=Column(String(255))
    progress_status=Column(String(255))
    occupancy=Column(String(255))
    vehicle_id=Column(String(255))
    gtfs_block_id=Column(String(255))

    def __repr__(self):
        output = ''
        for var, val in vars(self).items():
            if var == '_sa_instance_state':
                continue
            else:
                output = output + ('{} {} '.format(var,val))
        return output

    def __init__(self,route,db_url,timestamp):
        self.route_simple = route
        self.timestamp = timestamp
        engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(engine) # make sure the table exists every time an instance is created