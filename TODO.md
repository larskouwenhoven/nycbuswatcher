# todo

1. finish API
    - system API (bulk query)
        - requires a datetime range in in ISO 8601 like `/trips&start=2020-08-11T14:42:00+00:00&end=2020-08-11T15:12:00+00:00` per [urschrei](https://twitter.com/urschrei/status/1309473665789165569)
        - use query filter to enforce a maximum interval of 1 hour? (for now)
        - returns all fields (for now)
    - keplerized endpoints

# final deployment

1. decide what commit to deploy

2. deploy and observe

3. stop EC2 instance

4. export data from EC2

5. import EC2 data into Cornell instance



# debugging

*connect to mysql inside a container* to start a mysql client inside a mysql docker container

```
docker exec -it nycbuswatcher_db_1 mysql -uroot -p buses
[root password=bustime]
```

quick diagnostic query for how many records per day—`SELECT service_date, COUNT(*) FROM buses GROUP BY service_date;`

query how many by date/hour/minute—`SELECT service_date, date_format(timestamp,'%Y-%m-%d %H-%i'), COUNT(*) FROM buses GROUP BY service_date, date_format(timestamp,'%Y-%m-%d %H-%i');`

#### create conda env

`conda env export --from-history >environment.new.yml`
