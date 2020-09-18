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


# use

### grabber.py


```python
python grabber.py -r M1
python grabber.py -r ALL
```

##### todo (descending importance)
1. add parsing for the MonitoredCall portion of API response for each bus (currently discarded)
5. db optimization to reduce size
6. db optimization improve query performance
1. add ability to (batch) re-process archived files 


# development


### additional data scrapers

1. stop monitoring—[SIRIStopMonitoring](http://bustime.mta.info/wiki/Developers/SIRIStopMonitoring) reports info on individual stops, 1 at a time only.
2. route geometry from [OneBusAway API](http://bustime.mta.info/wiki/Developers/OneBusAwayRESTfulAPI) (much easier than working with the GTFS) on:
- The list of routes covered by MTA Bus Time
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


