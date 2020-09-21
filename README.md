# NYC MTA BusTime Scraper
#### v0.1 2020 Sept 20
Anthony Townsend <atownsend@cornell.edu>

# function

Fetches list of active routes from OneBusAway API, then cycles through and fetches current vehicle positions for all buses operating on these routes. This avoids the poor performance of trying to grab the entire system feed from the BusTime API. Dumps full API response (for later reprocessing to extract additional data) to compressed individual files and most of the vehicle status fields to mysql table (the upcoming stop data is omitted from the database dump for now).


# install

1. clone the repo
2. obtain an API key from http://bustime.mta.info/wiki/Developers/Index/ and put it in .env
    ```
    # .env example
    API_KEY = fasjhfasfajskjrwer242jk424242
    ```
3. mysql setup (optional)
    ```sql
    CREATE DATABASE buses;
    USE buses;
    CREATE USER 'nycbuswatcher'@'localhost' IDENTIFIED BY 'bustime';
    GRANT ALL PRIVILEGES ON * . * TO 'nycbuswatcher'@'localhost';
    FLUSH PRIVILEGES;
 
    ```
3. run
    ```python
    python grabber2.py # development: run once and quite
    python grabber2.py -p # production: runs in infinite loop at set interval using scheduler (hardcoded for now)
    ```

##### todo (descending importance)
1. use `asyncio` to speed up feed downloads
1. add parsing for the MonitoredCall portion of API response for each bus (currently discarded)
2. db optimization to reduce size (VARCHAR lengths)
3. db optimization improve query performance
4. add ability to (batch) re-process archived files through parser, db_dump

# development


### additional data scrapers

1. stop monitoring—[SIRIStopMonitoring](http://bustime.mta.info/wiki/Developers/SIRIStopMonitoring) reports info on individual stops, 1 at a time only.
2. route geometry from [OneBusAway API](http://bustime.mta.info/wiki/Developers/OneBusAwayRESTfulAPI) (much easier than working with the GTFS) on:
- Full information about each stop covered by MTA Bus Time (e.g. the lat/lon coordinates, stop name, list of routes serving that stop)
- The stops served by a given route
- The physical geometry for a given route (for mapping and geographic calculations)
- The schedule of trips serving a given stop or route (repeat: schedule, having nothing to do with the real-time data)
- The stops or routes near a given location


### internal api

Deploy an api using flask or FastAPI to expose database for our own dashboard and applications.

### dashboard

build off:
- OneBusAway API (geometry, don't store it)
- our internal API for historical bus location / arrival data

platform?
- kepler.gs
- dash/plotly


