# todo

1. system API
    - bulk query
        - requires a datetime range in in ISO 8601 like `/trips&start=2020-08-11T14:42:00+00:00&end=2020-08-11T15:12:00+00:00` per [urschrei](https://twitter.com/urschrei/status/1309473665789165569)
        - use query filter to enforce a maximum interval of 1 hour? (for now)
        - returns all fields (for now)

2. front end
    - base template and index.html template (using bootstrap-flask)
    - JS map app
        - street base map (from Stamen?)
        - points layer, geojson from /api/v1/nyc/livemap (last 60 seconds) — mapbox [tutorial](https://docs.mapbox.com/mapbox-gl-js/example/geojson-markers/)

3. keplerized endpoints


# debugging reference

### database
*connect to mysql inside a container* to start a mysql client inside a mysql docker container

```
docker exec -it nycbuswatcher_mysql_docker_1 mysql -uroot -p buses
[root password=bustime]
```

quick diagnostic query for how many records per day—`SELECT service_date, COUNT(*) FROM buses GROUP BY service_date;`

query how many by date/hour/minute—`SELECT service_date, date_format(timestamp,'%Y-%m-%d %H-%i'), COUNT(*) FROM buses GROUP BY service_date, date_format(timestamp,'%Y-%m-%d %H-%i');`