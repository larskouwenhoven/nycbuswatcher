# from sqlalchemy import *
from sqlalchemy import Column, Date, DateTime, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from datetime import datetime

Base = declarative_base()

class BusObservation(Base): # todo optimize STRING field lengths
    __tablename__ = "buses"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime) #todo check inputs and convert to DateTime
    route_simple=Column(String(255)) #this is the route name passed through from the command line, may or may not match route_short
    route_long=Column(String(255))
    direction=Column(String(255))
    service_date=Column(String(255)) #todo check inputs and convert to Date
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

    # def __repr__(self):# todo repr
    #    return (f'{self.__class__.__name__}('
    #            f'{self.color!r}, {self.mileage!r})')

    def __init__(self, route,db_url):
        self.route_simple = route
        self.timestamp = datetime.now()
        engine = create_engine(db_url, echo=True)
        Base.metadata.create_all(engine) # make sure the table exists every time an instance is created