FROM tiangolo/uwsgi-nginx-flask:python3.7

# RUN apt-get update -y; apt-get upgrade -y; apt-get install -y default-libmysqlclient-dev python-dev gcc python3-pip
RUN apt-get update -y; apt-get upgrade -y; apt-get install -y python3-pip

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN /usr/bin/pip3 install flask flask-restful marshmallow

# todo load env file that remaps the db hostname

COPY . /api

