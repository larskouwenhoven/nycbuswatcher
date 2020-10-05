# todo

1. debug docker flask --> db connection
    - is the time/timezone different in the different containers?
    - seems like it might just be a problem with the NOW - 60 seconds part of the query?

2. route maps for front end
    - combine them into a single file?
    - make the geojson accessible via the API
    - add layer(s) to the Javascript map on index.html
    - create a scheduler job to update them daily at 2am (in a temp folder, only copying over if successful and backing up the old one)
 
3. API
    - system API (bulk query)
        - requires a datetime range in in ISO 8601 like `/trips&start=2020-08-11T14:42:00+00:00&end=2020-08-11T15:12:00+00:00` per [urschrei](https://twitter.com/urschrei/status/1309473665789165569)
        - use query filter to enforce a maximum interval of 1 hour? (for now)
        - returns all fields (for now)
    - keplerized endpoints

4. project refactor
    - once everything is working, mark a release 
    - work out lib import path issues in the project generally (what are best practices?)   
    - having Database in the app folder is weird and bad
   

### debugging reference

s*connect to mysql inside a container* to start a mysql client inside a mysql docker container

```
docker exec -it nycbuswatcher_db_1 mysql -uroot -p buses
[root password=bustime]
```

quick diagnostic query for how many records per day—`SELECT service_date, COUNT(*) FROM buses GROUP BY service_date;`

query how many by date/hour/minute—`SELECT service_date, date_format(timestamp,'%Y-%m-%d %H-%i'), COUNT(*) FROM buses GROUP BY service_date, date_format(timestamp,'%Y-%m-%d %H-%i');`