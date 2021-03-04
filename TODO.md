# Cornell Tech Spring 2021 Specialization Project

#### who
- supervisor: anthony townsend
- students: jamie geng, jeremy shaffer

#### links
- [BusTime](https://bustime.mta.info/wiki/Developers/SIRIIntro)
- [NYCbuswatcher app](http://nyc.buswatcher.org)
- [NYCbuswatcher repo](https://github.com/anthonymobile/nycbuswatcher)
- [NYC bus data working Group](https://github.com/Bus-Data-NY)

#### feb 12 — week 1 — orientation, the API
- pick new meeting time (not Fridays)
- the NYCbuswatcher app
- the NYCbuswatcher repo
- the BusTime APIs — query and response
- a look at the data — what can we see in the data?
- assignment A: 1 page of goals and objectives, what do we want to produce by end of semester? year? think of a question you want to research in addition to technical skills
- assignment B: register at MTA for a BusTime API key, and subscribe to the Google Groups for MTA developers
 
### feb 19 — week 2
- review goals and objectives

### feb 26 — week 3
- review draft proposal

### mar 5 — week 4 — 

- final review of project proposals DUE TODAY
- welcome to Slack
- assignment: setting up development environment
    - database 
        - install Docker and postgis docker stack (https://hub.docker.com/r/kartoza/postgis/)
            - make a copy of `https://github.com/kartoza/docker-postgis/blob/develop/docker-compose.yml`
                - change `POSTGRES_DB=buses` and `POSTGRES_DBNAME=buses`
            - start the stack with `docker-compose up -d `
            - test it
                - if you have a postgres CLI client, connect with `psql -h localhost buses`
                - else install a postgres client (Mac: [Postgres.app](https://postgresapp.com/))
                - note if you have another database server running like mysql on port 5432 this will conflict (usually the stack wont start, so shut the other service down ior change the port in the `docker-compose.yml`)
    - [Bus Data Working Group tools](https://github.com/Bus-Data-NYC)
        - install the [mta-bus-archive](https://github.com/Bus-Data-NYC/mta-bus-archive) retrieval tool
        ```git clone https://github.com/Bus-Data-NYC/mta-bus-archive.git```
            - i only just realized we can also use this for real-time data!
            - if you are using the docker container above, use these values for  
                ```
                PGDATABASE=buses
                PGUSER=docker
                PGPASSWORD=docker
                PGHOST=localhost
                ```
                (you may need to use the `export PGDATABASE=buses` shell command )
            - grab one or more day's worth of data
                - `make download DATE=2020-12-11` (my birthday!)
        - on your own
            - install Juypter notebook and pandas
            - see if you can get a connection from the python notebook in Juypter to the database to retrieve some data
                - literal (https://blog.panoply.io/connecting-jupyter-notebook-with-postgresql-for-python-data-analysis)
                - more seamless/elegant (https://medium.com/analytics-vidhya/postgresql-integration-with-jupyter-notebook-deb97579a38d)
            


### mar 12 — week 5 — 
- troubleshooting the toolkit
- initial data exploration
- milestone review, what needs doing over next 2 weeks?

### mar 19 — ANTHONY VACATION

### mar 26 — week 6 — 
- mid-term milestone: some external review by CT faculty

### apr 2 — week 7 — 
### apr 9 — week 8 — 
### apr 16 — week 9 — 
### apr 23 — WELLNESS DAY 
### apr 30 — week 10 — 
### may 7 — week 11 — 
### may 14 — week 12 — 
- final milestone: some external review by CT faculty
- may 17 final report due
### may 21 - week 13 -
- possible post-deadline wrapup session

### fall 2021 planning
- parking lot


## master to-do list for NYCbuswatcher 
Can draw on these for our project steps as we have time/interest/relevance.

- #### SMALL
    - add ability to (batch) re-process archived JSON files through parser, db_dump

- #### BIG
    - rebuild entire front end as a Gatsby app (using the [gatsby-starter-mapbox](https://github.com/anthonymobile/gatsby-starter-mapbox) and [gatsby-start-mapbox-examples](https://github.com/astridx/gatsby-starter-mapbox-examples) templates)
    - finish API
        - bulk query API for all buses in the system during {time period}
            - requires a datetime range in in ISO 8601 like `/trips&start=2020-08-11T14:42:00+00:00&end=2020-08-11T15:12:00+00:00` per [urschrei](https://twitter.com/urschrei/status/1309473665789165569)
            - use query filter to enforce a maximum interval of 1 hour? (for now)
            - returns all fields (for now)
        - keplerized endpoints?

- #### MEDIUM
    - additional data scrapers
        - add parsing for the MonitoredCall portion of API response for each bus (currently discarded)
        - stop monitoring—[SIRIStopMonitoring](http://bustime.mta.info/wiki/Developers/SIRIStopMonitoring) reports info on individual stops, 1 at a time only.
        - route geometry from [OneBusAway API](http://bustime.mta.info/wiki/Developers/OneBusAwayRESTfulAPI) (much easier than working with the GTFS) on:
            - Full information about each stop covered by MTA Bus Time (e.g. the lat/lon coordinates, stop name, list of routes serving that stop)
            - The stops served by a given route
            - The physical geometry for a given route (for mapping and geographic calculations) **MTA endpoint appears to be inoperative**
            - The schedule of trips serving a given stop or route (repeat: schedule, having nothing to do with the real-time data)
            - The stops or routes near a given location


## debugging tips (NYCbuswatcher only)

### mysql

#### useful queries
- quick diagnostic query for how many records per day—`SELECT service_date, COUNT(*) FROM buses GROUP BY service_date;`
- query how many by date/hour/minute—`SELECT service_date, date_format(timestamp,'%Y-%m-%d %H-%i'), COUNT(*) FROM buses GROUP BY service_date, date_format(timestamp,'%Y-%m-%d %H-%i');`

#### dockerized mysql

- *connect to mysql inside a container* to start a mysql client inside a mysql docker container
    ```
    docker exec -it nycbuswatcher_db_1 mysql -uroot -p buses
    [root password=bustime]
    ```

