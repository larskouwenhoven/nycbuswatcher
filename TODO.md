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

1. final review of project proposals DUE TODAY
2. welcome to Slack
3. assignment: setting up development environment + get the data
    1. come up with a way to grab a month's worth of data According to the [mta-bus-archive](https://github.com/Bus-Data-NYC/mta-bus-archive) tool: "Bus position data for July 2017 forward is archived at `https://s3.amazonaws.com/nycbuspositions`. Archive files follow the pattern `https://s3.amazonaws.com/nycbuspositions/YYYY/MM/YYYY-MM-DD-bus-positions.csv.xz`, e.g. `https://s3.amazonaws.com/nycbuspositions/2017/07/2017-07-14-bus-positions.csv.xz`. i'd suggest writing a script to generate the urls. why not grab a whole year while you are at it...
    2. the data is in CSVs, so we can load it into pandas. i'd probably concatenate it into one giant file first though
    3. install Juypter notebook and pandas


### mar 12 — week 5
- troubleshooting the toolkit
- initial data exploration
- milestone review, what needs doing over next 2 weeks?

### mar 19 — ANTHONY VACATION

### mar 26 — week 6
- mid-term milestone: some external review by CT faculty

### apr 2 — week 7
### apr 9 — week 8
### apr 16 — week 9
### apr 23 — WELLNESS DAY 
### apr 30 — week 10
### may 7 — week 11
### may 14 — week 12
- final milestone: some external review by CT faculty
- may 17 final report due
### may 21 - week 13
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

