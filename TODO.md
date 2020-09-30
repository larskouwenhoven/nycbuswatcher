# todo

1. build out NOW map
    - API endpoint, GEOJSON feauture collection of Points of all unique vehicle_id observations from last n90? seconds
    - map app
        1. new (or run in api.py?) flask-bootstrap app 
        2. html page
        3. JS map app showing all markers on an NYC map [tutorial](https://docs.mapbox.com/mapbox-gl-js/example/geojson-markers/)
2. kepler endpoint
    - finish and test
3. wide open endpoint
    - bulk with few restrictions on date, route, etc but fewer fields
    - per [urschrei](https://twitter.com/urschrei/status/1309473665789165569). "simplest approach is to allow optional from and to parameters in ISO 8601, 
        so something like 
        ```
        /trips&from=2020-08-11T14:42:00+00:00&to=2020-08-11T15:12:00+00:00
        ```
        The format is easy to use on the client side and you can be as granular as you like / enforce max intervals server-side."


# debugging reference

### database
*connect to mysql inside a container* to start a mysql client inside a mysql docker container

```
docker exec -it nycbuswatcher_mysql_docker_1 mysql -uroot -p buses
[root password=bustime]
```

quick diagnostic query for how many records per day—`SELECT service_date, COUNT(*) FROM buses GROUP BY service_date;`

query how many by date/hour/minute—`SELECT service_date, date_format(timestamp,'%Y-%m-%d %H-%i'), COUNT(*) FROM buses GROUP BY service_date, date_format(timestamp,'%Y-%m-%d %H-%i');`