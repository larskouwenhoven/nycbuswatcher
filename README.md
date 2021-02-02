# NYC MTA BusTime Scraper
#### v1.1 2020 Oct 5
Anthony Townsend <atownsend@cornell.edu>

## function

Fetches list of active routes from MTA BusTime OneBusAway API via asynchronous http requests, then cycles through and fetches current vehicle positions for all buses operating on these routes. This avoids the poor performance of trying to grab the entire system feed from the MTA BusTime SIRI API. Dumps full API response (for later reprocessing to extract additional data) to compressed individual files and most of the vehicle status fields to mysql table (the upcoming stop data is omitted from the database dump for now). Fully dockerized, runs on scheduler 1x per minute. Data storage requirments ~ 1-2 Gb/day (guesstimate).


## installation 

### (docker)

1. clone the repo

    `git clone https://github.com/anthonymobile/nycbuswatcher.git`
    
2. obtain API keys and put them in .env
    - http://bustime.mta.info/wiki/Developers/Index/
    - MapBox

    ```txt
    API_KEY = fasjhfasfajskjrwer242jk424242'
    MAPBOX_API_KEY = pk.ey42424fasjhfasfajskjrwer242jk424242'
    ```
    
3. build and run the images

    ```
    cd nycbuswatcher
    docker-compose up -d --build
    ```

### (manual)

1. clone the repo

    `git clone https://github.com/anthonymobile/nycbuswatcher.git`
    
2. obtain an API key from http://bustime.mta.info/wiki/Developers/Index/ and put it in .env

    `echo 'API_KEY = fasjhfasfajskjrwer242jk424242' > .env`
    
3. create the database (mysql only, 5.7 recommended)
    ```sql
    CREATE DATABASE buses;
    USE buses;
    CREATE USER 'nycbuswatcher'@'localhost' IDENTIFIED BY 'bustime';
    GRANT ALL PRIVILEGES ON * . * TO 'nycbuswatcher'@'localhost';
    FLUSH PRIVILEGES;
 
    ```
3. run
    ```python
    python grabber.py # development: run once and quit
    python grabber.py -p # production: runs in infinite loop at set interval using scheduler (hardcoded for now)
    ```

## usage 

if you just want to test out the grabber, you can run `export PYTHON_ENV=development; python grabber.py -l` and it will run once, dump the responses to a pile of files, and quit after throwing a database connection error. (or not, if you did step 3 in "manual" above) 











