# many_get.py
# make a whole pile of api calls and store
# their response objects in a list.
# Using the homogeneous-session.
import requests
import os

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
            "/api/where/routes-for-agency/MTA%20NYCT.json?key={}&VehicleMonitoringDetailLevel=calls&LineRef={}".format(
                os.getenv("API_KEY"), route['id']))
    return path_list


path_list = get_path_list()

results = []

async def grabber(s,a_path):
    r = await s.get(path=a_path)
    results.append(r)

async def main(path_list):
    from asks.sessions import Session
    s = Session('http://bustime.mta.info', connections=20)
    async with trio.open_nursery() as n:
        for path in path_list:
            n.start_soon(grabber, s, path)


trio.run(main, path_list)

print(results)

