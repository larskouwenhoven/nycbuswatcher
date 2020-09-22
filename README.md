# NYC MTA BusTime Scraper
#### v0.1 2020 Sept 20
Anthony Townsend <atownsend@cornell.edu>

# function

Fetches list of active routes from OneBusAway API via asynchronous http requests, then cycles through and fetches current vehicle positions for all buses operating on these routes. This avoids the poor performance of trying to grab the entire system feed from the BusTime API. Dumps full API response (for later reprocessing to extract additional data) to compressed individual files and most of the vehicle status fields to mysql table (the upcoming stop data is omitted from the database dump for now).


# install

n.b. there is a working `docker-compose` script in the repo but it may be a little out of date/wobbly, and missing a few bits like the .env file which you'll have to copy over manually

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
    python grabber_async.py # development: run once and quite
    python grabber_async.py -p # production: runs in infinite loop at set interval using scheduler (hardcoded for now)
    ```



#todo 

##asap
1. finish/debug dockerization
2. add parsing for the MonitoredCall portion of API response for each bus (currently discarded)
3. optimization to speed up parsing + db i/o
    - not sure where the slowdown is
    - branch `new_parser` did not seem to help much (reversing the lookup table to reduce # of loops)
    - idea: separate feed grabber from parser. but will the parser ever catch up if it falls behind? (e.g. it takes longer to parse than the time between grabs)
    - more compute capacity?

## future
1. add ability to (batch) re-process archived files through parser, db_dump
2. additional data scrapers
    - stop monitoring—[SIRIStopMonitoring](http://bustime.mta.info/wiki/Developers/SIRIStopMonitoring) reports info on individual stops, 1 at a time only.
    - route geometry from [OneBusAway API](http://bustime.mta.info/wiki/Developers/OneBusAwayRESTfulAPI) (much easier than working with the GTFS) on:
        - Full information about each stop covered by MTA Bus Time (e.g. the lat/lon coordinates, stop name, list of routes serving that stop)
        - The stops served by a given route
        - The physical geometry for a given route (for mapping and geographic calculations)
        - The schedule of trips serving a given stop or route (repeat: schedule, having nothing to do with the real-time data)
        - The stops or routes near a given location
3. internal api
    - Deploy an api using flask or FastAPI to expose database for our own dashboard and applications.

4. dashboard
    - geometry: OneBusAway API ( don't handle/store the GTFS locally)
    - data: our internal API, historical location + arrival
    - renderer: kepler.js or dash/plotly


