# many_get.py
# make a whole pile of api calls and store
# their response objects in a list.
# Using the homogeneous-session.
import requests
import os
from datetime import datetime
import json
import sys
import time
import gzip

import Database as db

from dotenv import load_dotenv
load_dotenv()

import trio


def get_path_list():
    path_list = []
    url = "http://bustime.mta.info/api/where/routes-for-agency/MTA%20NYCT.json?key=" + os.getenv("API_KEY")
    response = requests.get(url, timeout=30)
    routes = response.json()
    print(
        'Found {} routes. Fetching current positions with ASYNCHRONOUS requests...'.format(len(routes['data']['list'])))
    for route in routes['data']['list']:
        path_list.append(
            {route['id']:"/api/where/routes-for-agency/MTA%20NYCT.json?key={}&VehicleMonitoringDetailLevel=calls&LineRef={}".format(os.getenv("API_KEY"), route['id'])}
        )
    return path_list #bug host not found error bustime.mta.info, catch wait 3-5 sec and try again


def dump_to_screen(feeds):
    for route_bundle in feeds:
        for route_id, data in route_bundle.items():
            print (data.json())
    return

def dump_to_file(feeds):
    path = ("data/")
    check = os.path.isdir(path)
    if not check:
        os.makedirs(path)
        print("created folder : ", path)
    else:
        pass
    date = datetime.now().strftime("%Y-%m-%dT_%H:%M:%S.%f")
    for route_bundle in feeds:
        for route_id,route_report in route_bundle.items():

            # uncompressed version
            dumpfile=(path + route_id.split()[1] + '_' + date +'.json')
            with open(dumpfile, 'w') as json_file:
               json.dump(route_report.json(), json_file, indent=4)

            # todo add compression
            # https://medium.com/@busybus/zipjson-3ed15f8ea85d

    return

def dump_to_db(dbparams,feeds): # todo debug database

    session,db_url = db.get_session(dbparams)
    print('Dumping to {}'.format(db_url))
    for route_bundle in feeds:
        # sys.stdout.write(' <{}> '.format(str(next(iter(route_bundle)))))
        for route_id,route_report in route_bundle.items():
            for bus in db.parse_buses(route_id, route_report.json(), db_url):
                session.add(bus)
        session.commit()
    return




if __name__ == "__main__":
    start = time.time()

    # todo add production switch + chane dbhost to 'mysql_docker'
    # todo add scheduler

    dbparams = {
        'dbname': 'buses',
        'dbuser': 'nycbuswatcher',
        'dbpassword': 'bustime',
        'dbhost':'localhost'
    }

    path_list = get_path_list()

    feeds = []

    async def grabber(s,a_path,route_id):
        r = await s.get(path=a_path)
        feeds.append({route_id:r})

    async def main(path_list):
        from asks.sessions import Session
        s = Session('http://bustime.mta.info', connections=20)
        async with trio.open_nursery() as n:
            for path_bundle in path_list:
                for route_id,path in path_bundle.items():
                    n.start_soon(grabber, s, path, route_id )


    trio.run(main, path_list) # bug ValueError: 'bustime.mta.info' does not appear to be an IPv4 or IPv6 address

    # dump_to_screen(feeds)
    dump_to_file(feeds)
    dump_to_db(dbparams, feeds)

    end = time.time()
    print('\nFetched {} routes in {:2f} seconds to uncompressed archive and database.'.format(len(feeds),(end - start)))



