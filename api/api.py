# adapted from https://www.codementor.io/@sagaragarwal94/building-a-basic-restful-api-in-python-58k02xsiq
# query parameter handling after https://stackoverflow.com/questions/30779584/flask-restful-passing-parameters-to-get-request

# v1 hard code queries (this)
# future v2 use SQLalchemy ORM
# future v3 port to FastAPI w/ async/await

from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api
# from sqlalchemy import create_engine

from Database import *
from marshmallow import Schema, fields

dbparams = {
    'dbname': 'buses',
    'dbuser': 'nycbuswatcher',
    'dbpassword': 'bustime',
    'dbhost': 'localhost'
}


db_connect = create_engine(get_db_url(dbparams))
app = Flask(__name__)
api = Api(app)

def unpack_query_results(query):
    return [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

def query_builder(parameters):
    query_suffix = ''
    for field, value in parameters.items():
        query_suffix = query_suffix + '{} = "{}" AND '.format(field,value)
    query_suffix=query_suffix[:-4] # strip tailing ' AND'
    return query_suffix

# after https://geoffboeing.com/2015/10/exporting-python-data-geojson/
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

#--- LIST ALL UNIQUE ROUTES IN HISTORY ---#
class Routes(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("SELECT DISTINCT route_short FROM buses")
        results = {'routes': [i[0] for i in query.cursor.fetchall()]}
        return jsonify(results)

# #--- ALL OBSERVATIONS IN HISTORY FOR SINGLE ROUTE ---#
# class FullHistory(Resource):
#     def get(self,route_id):
#         conn = db_connect.connect()  # connect to database
#         query = conn.execute("SELECT * FROM buses WHERE route_short='{}'".format(route_id))
#         # result = {'observations': query.cursor.fetchall()}
#         results = {'observations': unpack_query_results(query)}
#         return jsonify(results) # todo geojsonized this into a list or dict of GEOJSON Points


#--- ALL OBSERVATIONS ON A SINGLE TRIP, IN GEOJSON ---#

class TripQuerySchema(Schema):
    service_date = fields.Str(required=True)
    trip_id = fields.Str(required=True)

trip_schema = TripQuerySchema()

class TripAPI(Resource): #todo all points for a specific trip  returned as a GEOJSON LineString
    def get(self):
        errors = trip_schema.validate(request.args)
        if errors:
            abort(400, str(errors))
        conn = db_connect.connect()  # connect to database

        query_suffix = query_builder(request.args)

        query = conn.execute("SELECT * FROM buses WHERE {}".format(query_suffix ))
        results = {'observations': unpack_query_results(query)}
        return jsonify(results)
        # return results_to_geojson_LineString(results)




#--- URLS ---#
api.add_resource(Routes, '/api/v1/nyc/routes')
api.add_resource(TripAPI, '/api/v1/nyc/trips', endpoint='trips')



if __name__ == '__main__':
    # app.run(port='5002')
    app.run(debug=True)