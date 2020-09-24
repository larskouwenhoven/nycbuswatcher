# adapted from https://www.codementor.io/@sagaragarwal94/building-a-basic-restful-api-in-python-58k02xsiq

# v1 hard code queries
# v2 use SQLalchemy ORM
# v3 port to FastAPI w/ async/await

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

from Database import *

dbparams = {
    'dbname': 'buses',
    'dbuser': 'nycbuswatcher',
    'dbpassword': 'bustime',
    'dbhost': 'localhost'
}


# response_fields = '   route_simple, route_long, direction, service_date,trip_id,gtfs_shape_id,route_short,agency,origin_id,destination_id,destination_name,alert, lat, lon, bearing,progress_rate,progress_status, occupancy, vehicle_id,gtfs_block_id'

db_connect = create_engine(get_db_url(dbparams))
app = Flask(__name__)
api = Api(app)

def unpack_results(query):
    return [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

#--- /api/v1/nyc/routes -------------------------------------------------------
class Routes(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("SELECT DISTINCT route_short FROM buses")
        result = {'routes': [i[0] for i in query.cursor.fetchall()]}
        return jsonify(result)

api.add_resource(Routes, '/api/v1/nyc/routes')


#--- /api/v1/nyc/routes/<route_id> --------------------------------------------
class FullHistory(Resource):
    def get(self,route_id):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("SELECT * FROM buses WHERE route_short='{}'".format(route_id))
        # result = {'observations': query.cursor.fetchall()}
        result = {'observations': unpack_results(query)}

        return jsonify(result)

api.add_resource(FullHistory, '/api/v1/nyc/routes/<string:route_id>')


#--- /api/v1/nyc/routes/<route_id>/<yyyy-mm-dd> -------------------------------
class HistoryByDate(Resource):
    def get(self,route_id,date):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("SELECT * FROM buses WHERE route_short='{}' AND service_date='{}'".format(route_id,date))
        result = {'observations': unpack_results(query)}
        return jsonify(result)

api.add_resource(HistoryByDate, '/api/v1/nyc/routes/<string:route_id>/<string:date>')


# todo add additional routes
# todo find out what kepler wants from API and start to build towards it




# quick diagnostic for how many records per day
# SELECT service_date, COUNT(*) FROM buses GROUP BY service_date;
#
# how many by date/hour/minute
# SELECT service_date, date_format(timestamp,'%Y-%m-%d %H-%i'), COUNT(*) FROM buses GROUP BY service_date, date_format(timestamp,'%Y-%m-%d %H-%i');
#



# api.add_resource(Tracks, '/tracks')  # Route_2
# api.add_resource(Employees_Name, '/employees/<employee_id>')  # Route_3


# class Tracks(Resource):
#     def get(self):
#         conn = db_connect.connect()
#         query = conn.execute("select trackid, name, composer, unitprice from tracks;")
#         result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
#         return jsonify(result)
#
#
# class Employees_Name(Resource):
#     def get(self, employee_id):
#         conn = db_connect.connect()
#         query = conn.execute("select * from employees where EmployeeId =%d " % int(employee_id))
#         result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
#         return jsonify(result)



if __name__ == '__main__':
    # app.run(port='5002')
    app.run(debug=True)