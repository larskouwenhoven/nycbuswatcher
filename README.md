## install

1. clone the repo
2. obtain an API key from http://bustime.mta.info/wiki/Developers/Index/ and put it in .env

## use

### grabber.py


```python
python grabber.py -r M1
python grabber.py -r all
```

1. debug routelist grabber
2. write parser for bus feed fetcher
3. database connection ([sqlite w/ SQLalchemyORM for now?](https://medium.com/@mahmudahsan/how-to-use-python-sqlite3-using-sqlalchemy-158f9c54eb32))
4. dockerize deployment


### dashboard.py (future)
1. parse the GTFS for the routes http://bustime.mta.info/wiki/Developers/SIRIIntro
2. view and query data on a map
    - dash/plotly
    - kepler?


### testfeed_get_bus_info.py

Forked from [https://github.com/praveenashokkumar/MTA_Bus_Tracker](https://github.com/praveenashokkumar/MTA_Bus_Tracker). See there for docs.

```python
python testfeed_get_bus_info.py M1 M1.csv

      Bus Line : B52
        Number of Active Buses : 5
        Bus 0 is at latitude 40.687241 and longitude -73.941661
        Bus 1 is at latitude 40.690822 and longitude -73.920759
        Bus 2 is at latitude 40.688363 and longitude -73.979563
        Bus 3 is at latitude 40.688282 and longitude -73.979356
        Bus 4 is at latitude 40.686839 and longitude -73.964694
```


### testfeed_show_bus_locations.py

Forked from [https://github.com/praveenashokkumar/MTA_Bus_Tracker](https://github.com/praveenashokkumar/MTA_Bus_Tracker). See there for docs.

```python
python testfeed_show_bus_locations.py M1

        Latitude,Longitude,Stop Name,Stop Status
          40.755489,-73.987347,7 AV/W 41 ST,at stop
          40.775657,-73.982036,BROADWAY/W 69 ST,approaching
          40.808332,-73.944979,MALCOLM X BL/W 127 ST,approaching
          40.764998,-73.980416,N/A,N/A
          40.804702,-73.947620,MALCOLM X BL/W 122 ST,< 1 stop away
          40.776950,-73.981983,AMSTERDAM AV/W 72 ST,< 1 stop away
          40.737650,-73.996626,AV OF THE AMERICAS/W 18 ST,< 1 stop away
```

