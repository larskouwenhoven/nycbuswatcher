# todo

1. finish and test geojson bundler for TripAPI
2. build out another API for bulk grab to front end... no restrictions on date, route, etc but fewer fields
3. build a couple of endpoints for starter views, e.g. what the front-end needs to load to render 1st view (e.g. all the buses in the last hour? day? week?)


# debugging tips



## connect to mysql inside a container
to start a mysql client inside a mysql docker container

docker exec -it nycbuswatcher_mysql_docker_1 mysql -uroot -p buses
[root password=bustime]

quick diagnostic for how many records per day
SELECT service_date, COUNT(*) FROM buses GROUP BY service_date;

how many by date/hour/minute
SELECT service_date, date_format(timestamp,'%Y-%m-%d %H-%i'), COUNT(*) FROM buses GROUP BY service_date, date_format(timestamp,'%Y-%m-%d %H-%i');
