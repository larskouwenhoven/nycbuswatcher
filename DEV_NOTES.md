
# debugging tips
to start a mysql client inside a mysql docker container

docker exec -it nycbuswatcher_mysql_docker_1 mysql -uroot -p buses
[root password=bustime]

quick diagnostic for how many records per day
SELECT service_date, COUNT(*) FROM buses GROUP BY service_date;

how many by date/hour/minute
SELECT service_date, date_format(timestamp,'%Y-%m-%d %H-%i'), COUNT(*) FROM buses GROUP BY service_date, date_format(timestamp,'%Y-%m-%d %H-%i');




# debugging
 
1. look at `Database.parse_buses` to see where i am using a list index and where it might be going wrong (seems to on every route, so do a debug session and inspect manually)

```
2020-09-22 13:50:49,841 INFO sqlalchemy.engine.base.Engine BEGIN (implicit)
2020-09-22 13:50:49,841 INFO sqlalchemy.engine.base.Engine INSERT INTO buses (timestamp, route_simple, route_long, direction, service_date, trip_id, gtfs_shape_id, route_short, agency, origin_id, destination_id, destination_name, alert, lat, lon, bearing, progress_rate, progress_status, occupancy, vehicle_id, gtfs_block_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
2020-09-22 13:50:49,841 INFO sqlalchemy.engine.base.Engine (datetime.datetime(2020, 9, 22, 13, 49, 28, 577321), 'MTA NYCT_M116', 'MTA NYCT_M116', '1', '2020-09-22', 'MTA NYCT_MV_D0-Weekday-080200_M116_713', 'MTA_M1160060', 'M116', 'MTA NYCT', 'MTA_401998', 'MTA_401977', 'WEST SIDE BROADWAY-106 ST CROSSTOWN', None, 40.800604, -73.966112, 157.45694, 'normalProgress', None, None, 'MTA NYCT_4009', 'MTA NYCT_MV_D0-Weekday_C_MV_44880_M116-713')
2020-09-22 13:50:49,842 INFO sqlalchemy.engine.base.Engine INSERT INTO buses (timestamp, route_simple, route_long, direction, service_date, trip_id, gtfs_shape_id, route_short, agency, origin_id, destination_id, destination_name, alert, lat, lon, bearing, progress_rate, progress_status, occupancy, vehicle_id, gtfs_block_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
2020-09-22 13:50:49,842 INFO sqlalchemy.engine.base.Engine (datetime.datetime(2020, 9, 22, 13, 49, 28, 577321), 'MTA NYCT_M116', 'MTA NYCT_M116', '0', '2020-09-22', 'MTA NYCT_MV_D0-Weekday-081800_M116_705', 'MTA_M1160061', 'M116', 'MTA NYCT', 'MTA_404911', 'MTA_803059', 'EAST HARLEM PALADINO AV CROSSTOWN', None, 40.800499, -73.960121, 53.56914, 'normalProgress', None, None, 'MTA NYCT_3957', 'MTA NYCT_MV_D0-Weekday_C_MV_43680_M116-705')
2020-09-22 13:50:49,843 INFO sqlalchemy.engine.base.Engine INSERT INTO buses (timestamp, route_simple, route_long, direction, service_date, trip_id, gtfs_shape_id, route_short, agency, origin_id, destination_id, destination_name, alert, lat, lon, bearing, progress_rate, progress_status, occupancy, vehicle_id, gtfs_block_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
2020-09-22 13:50:49,845 INFO sqlalchemy.engine.base.Engine (datetime.datetime(2020, 9, 22, 13, 49, 28, 577321), 'MTA NYCT_M116', 'MTA NYCT_M116', '0', '2020-09-22', 'MTA NYCT_MV_D0-Weekday-078800_M116_703', 'MTA_M1160061', 'M116', 'MTA NYCT', 'MTA_404911', 'MTA_803059', 'EAST HARLEM PALADINO AV CROSSTOWN', None, 40.797375, -73.930664, 156.94173, 'noProgress', 'layover', None, 'MTA NYCT_3867', 'MTA NYCT_MV_D0-Weekday_C_MV_26700_M116-710')
2020-09-22 13:50:49,849 INFO sqlalchemy.engine.base.Engine INSERT INTO buses (timestamp, route_simple, route_long, direction, service_date, trip_id, gtfs_shape_id, route_short, agency, origin_id, destination_id, destination_name, alert, lat, lon, bearing, progress_rate, progress_status, occupancy, vehicle_id, gtfs_block_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
2020-09-22 13:50:49,849 INFO sqlalchemy.engine.base.Engine (datetime.datetime(2020, 9, 22, 13, 49, 28, 577321), 'MTA NYCT_M116', 'MTA NYCT_M116', '1', '2020-09-22', 'MTA NYCT_MV_D0-Weekday-081200_M98_904', 'MTA_M1160060', 'M116', 'MTA NYCT', 'MTA_401998', 'MTA_401977', 'WEST SIDE BROADWAY-106 ST CROSSTOWN', None, 40.804954, -73.956658, 157.184, 'normalProgress', None, None, 'MTA NYCT_4267', 'MTA NYCT_MV_D0-Weekday_C_MV_17400_M116-702')
2020-09-22 13:50:49,852 INFO sqlalchemy.engine.base.Engine INSERT INTO buses (timestamp, route_simple, route_long, direction, service_date, trip_id, gtfs_shape_id, route_short, agency, origin_id, destination_id, destination_name, alert, lat, lon, bearing, progress_rate, progress_status, occupancy, vehicle_id, gtfs_block_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
2020-09-22 13:50:49,853 INFO sqlalchemy.engine.base.Engine (datetime.datetime(2020, 9, 22, 13, 49, 28, 577321), 'MTA NYCT_M116', 'MTA NYCT_M116', '0', '2020-09-22', 'MTA NYCT_MV_D0-Weekday-079800_M116_707', 'MTA_M1160061', 'M116', 'MTA NYCT', 'MTA_404911', 'MTA_803059', 'EAST HARLEM PALADINO AV CROSSTOWN', None, 40.800239, -73.945467, 337.4054, 'normalProgress', None, None, 'MTA NYCT_3870', 'MTA NYCT_MV_D0-Weekday_C_MV_47280_M116-707')
2020-09-22 13:50:49,854 INFO sqlalchemy.engine.base.Engine INSERT INTO buses (timestamp, route_simple, route_long, direction, service_date, trip_id, gtfs_shape_id, route_short, agency, origin_id, destination_id, destination_name, alert, lat, lon, bearing, progress_rate, progress_status, occupancy, vehicle_id, gtfs_block_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
2020-09-22 13:50:49,854 INFO sqlalchemy.engine.base.Engine (datetime.datetime(2020, 9, 22, 13, 49, 28, 577321), 'MTA NYCT_M116', 'MTA NYCT_M116', '0', '2020-09-22', 'MTA NYCT_MV_D0-Weekday-080800_M116_710', 'MTA_M1160061', 'M116', 'MTA NYCT', 'MTA_404911', 'MTA_803059', 'EAST HARLEM PALADINO AV CROSSTOWN', None, 40.800525, -73.946154, 337.4054, 'normalProgress', None, None, 'MTA NYCT_3999', 'MTA NYCT_MV_D0-Weekday_C_MV_47880_M116-710')
2020-09-22 13:50:49,855 INFO sqlalchemy.engine.base.Engine COMMIT
list indices must be integers or slices, not str
list indices must be integers or slices, not str
```


# to do
1. separate feed2file grabber from file2db parser ? (10 seconds vs ?)

