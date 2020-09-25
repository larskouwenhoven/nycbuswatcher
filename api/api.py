# adapted from https://www.codementor.io/@sagaragarwal94/building-a-basic-restful-api-in-python-58k02xsiq

# v1 hard code queries
# v2 use SQLalchemy ORM
# v3 port to FastAPI w/ async/await

from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api
from sqlalchemy import create_engine
# from json import dumps

from Database import *
from marshmallow import Schema, fields

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


# setting up for the query parameter handling
# after https://stackoverflow.com/questions/30779584/flask-restful-passing-parameters-to-get-request




def unpack_query_results(query):
    return [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

def query_builder(parameters):
    query_suffix = ''
    for field, value in parameters.items():
        query_suffix = query_suffix + '{} = "{}" AND '.format(field,value)
    query_suffix=query_suffix[:-4] # strip tailing ' AND'
    return query_suffix

def results_to_geojson_Points(results):
    geojson = {'type': 'FeatureCollection', 'features': []}
    for row in results:
        feature = {'type': 'Feature',
                   'properties': {},
                   'geometry': {'type': 'Point',
                                'coordinates': []}}
        feature['geometry']['coordinates'] = [row['lat'], row['lon']]

        for k, v in row.items():
            feature['properties'][k] = row[v]
        geojson['features'].append(feature)
    return geojson

# #--- LIST ALL UNIQUE ROUTES IN HISTORY ---#
# class Routes(Resource):
#     def get(self):
#         conn = db_connect.connect()  # connect to database
#         query = conn.execute("SELECT DISTINCT route_short FROM buses")
#         results = {'routes': [i[0] for i in query.cursor.fetchall()]}
#         return jsonify(results)
#
# #--- ALL OBSERVATIONS IN HISTORY FOR SINGLE ROUTE ---#
# class FullHistory(Resource):
#     def get(self,route_id):
#         conn = db_connect.connect()  # connect to database
#         query = conn.execute("SELECT * FROM buses WHERE route_short='{}'".format(route_id))
#         # result = {'observations': query.cursor.fetchall()}
#         results = {'observations': unpack_query_results(query)}
#         return jsonify(results) # todo geojsonized this into a list or dict of GEOJSON Points
#
# #--- ALL OBSERVATIONS SINGLE DATE FOR SINGLE ROUTE ---#
# class RouteHistoryByDate(Resource):
#     def get(self,route_id,service_date):
#         conn = db_connect.connect()  # connect to database
#         query = conn.execute("SELECT * FROM buses WHERE route_short='{}' AND service_date='{}'".format(route_id,service_date))
#         results = {'observations': unpack_query_results(query)}
#         # return jsonify(results)
#         return results_to_geojson_Points(results) #todo test

# #--- LIST ALL TRIPS FOR A SINGLE DATE ALL ROUTES ---#
# class TripList(Resource):
#     def get(self,date):
#         conn = db_connect.connect()  # connect to database
#         query = conn.execute("SELECT DISTINCT service_date,trip_id FROM buses WHERE service_date='{}'".format(date))
#         results = {'trips': unpack_query_results(query)}
#         # return jsonify(results)
#         return results_to_geojson_Points(results) #todo test

# #--- ALL OBSERVATIONS ON A SINGLE TRIP AS GEOJSON POINTS ---#
# class TripDetails(Resource):
#     def get(self,service_date,trip_id):
#         conn = db_connect.connect()  # connect to database
#         query = conn.execute("SELECT * FROM buses WHERE service_date='{}' AND trip_id='{}'".format(service_date,trip_id))
#         results = {'observations': unpack_query_results(query)}
#         return jsonify(results) #todo all points for a specific trip  returned as a GEOJSON LineString


#USING QUERY PARAMETERS
# see https://stackoverflow.com/questions/30779584/flask-restful-passing-parameters-to-get-request

class TripQuerySchema(Schema):
    route_short = fields.Str(required=True)
    service_date = fields.Str(required=True)
    progress_status = fields.Str(required=False)
    vehicle_id = fields.Str(required=False)

trip_schema = TripQuerySchema()


class SimpleAPI(Resource):
    def get(self):
        errors = trip_schema.validate(request.args)
        if errors:
            abort(400, str(errors))
        conn = db_connect.connect()  # connect to database

        query_suffix = query_builder(request.args)

        # todo how do i access the args? from 'schema'?
        # bug todo build up the query from the args
        query = conn.execute("SELECT * FROM buses WHERE {}".format(query_suffix ))
        results = {'observations': unpack_query_results(query)}
        return jsonify(results)
        # return results_to_geojson_LineString(results) #todo all points for a specific trip  returned as a GEOJSON LineString


# api.add_resource(Routes, '/api/v1/nyc/routes')
# api.add_resource(FullHistory, '/api/v1/nyc/routes/<string:route_id>')
# api.add_resource(RouteHistoryByDate, '/api/v1/nyc/routes/<string:route_id>/<string:service_date>')
# api.add_resource(TripList, '/api/v1/nyc/trips/<string:service_date>')
# api.add_resource(TripDetails, '/api/v1/nyc/trips/<string:service_date>/<string:trip_id>')
api.add_resource(SimpleAPI, '/api/v1/nyc/trips', endpoint='trips')




if __name__ == '__main__':
    # app.run(port='5002')
    app.run(debug=True)