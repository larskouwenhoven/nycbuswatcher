
# debugging tips
to start a mysql client inside a mysql docker container

docker exec -it nycbuswatcher_mysql_docker_1 mysql -uroot -p buses
[root password=bustime]

quick diagnostic for how many records per day
SELECT service_date, COUNT(*) FROM buses GROUP BY service_date;


# to do

1. rewrite to load production/dev env from external and set globally?
2. write function to get list of routes from OBA API (test in python console)
2. Write an asynchronous loop to grab vehicles line by line
