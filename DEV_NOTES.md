
# debugging tips
to start a mysql client inside a mysql docker container

docker exec -it [container_name] mysql -uroot -p
[root password]

quick diagnostic for how many records per day
SELECT service_date, COUNT(*) FROM buses GROUP BY service_date;


# to do

1. update mysql docker to use volume as its data store
4. check data in EC2 mysql. (P mode M1). Test (P mode ALL)
1. rewrite to load production/dev env from external and set globally?
2. Write an asynchronous loop to grab vehicles line by line
