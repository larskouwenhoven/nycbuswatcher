
# debugging tips
to start a mysql client inside a mysql docker container

docker exec -it nycbuswatcher_mysql_docker_1 mysql -uroot -p buses
[root password=bustime]

quick diagnostic for how many records per day
SELECT service_date, COUNT(*) FROM buses GROUP BY service_date;

how many by date/hour/minute
SELECT service_date, date_format(timestamp,'%Y-%m-%d %H-%i'), COUNT(*) FROM buses GROUP BY service_date, date_format(timestamp,'%Y-%m-%d %H-%i');
