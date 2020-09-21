
# debugging tips
to start a mysql client inside a mysql docker container

docker exec -it nycbuswatcher_mysql_docker_1 mysql -uroot -p buses
[root password=bustime]

quick diagnostic for how many records per day
SELECT service_date, COUNT(*) FROM buses GROUP BY service_date;


# to do
3. load production/dev env from external and set globally?
4. move API key to a docker secret?


# rewrite the async version with asks/curio

# many_get.py
# make a whole pile of api calls and store
# their response objects in a list.
# Using the homogeneous-session.

import asks
import curio
asks.init('curio')

path_list = ['a', 'list', 'of', '1000', 'paths']

retrieved_responses = []

s = asks.Session('https://some-web-service.com',
                  connections=20)

async def grabber(a_path):
    r = await s.get(path=a_path)
    retrieved_responses.append(r)

async def main(path_list):
    for path in path_list:
        curio.spawn(grabber(path))

curio.run(main(path_list))

https://asks.readthedocs.io/en/latest/