
# debugging tips
to start a mysql client inside a mysql docker container

docker exec -it nycbuswatcher_mysql_docker_1 mysql -uroot -p buses
[root password=bustime]

quick diagnostic for how many records per day
SELECT service_date, COUNT(*) FROM buses GROUP BY service_date;


# to do
1. finish refactoring to condense fetch, parse, dump into one pipeline, and a loop around it populated by either a command line arg or a call to get_routelist
2. rewrite the fetch part as async
3. load production/dev env from external and set globally?
4. move API key to a docker secret?