import os
import json
import datetime


'''
from sqlalchemy import *
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# todo how to init each database once and only once?
# create tables
Base.metadata.create_all(engine)

class BusObservation(Base):
    """"""
    __tablename__ = "buses"

    #todo from http://bustime.mta.info/wiki/Developers/SIRIMonitoredVehicleJourney
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(String) # VehicleRef
    route = Column(String,10)
    lat=Column(Float) # VehicleLocation.Latitude
    lon=Column(Float) # VehicleLocation.Longitude
    bearing= Column(Float) # compass bearing, 0 = east, increments counterclockwise
    routename_short=Column(String) # PublishedLineName
    service_date=Column(Date) # DataFrameRef
    agency = Column(String)# OperatorRef
    destination = Column(String) # DestinationName

    # todo store everything else i can
    # todo optional to parse, add: ProgressRate, ProgressStatus, Occupancy,


    #todo
    def __init__(self, username, firstname, lastname, university):
        """"""
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.university = university

def get_session(route):

    engine = create_engine('sqlite:///data/{}_buses.db'.format(route), echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session



def dump_to_table(data, route):

    session=get_session(route)

    for b in data:

        user = BusObservation("james", "James", "Boogie", "MIT") #todo
        session.add(user)

    # commit the session the database
    session.commit()

    return
'''



def dump_to_json(data, route):

    # You should change 'test' to your preferred folder.
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
