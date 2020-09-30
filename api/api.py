# adapted from https://www.codementor.io/@sagaragarwal94/building-a-basic-restful-api-in-python-58k02xsiq
# query parameter handling after https://stackoverflow.com/questions/30779584/flask-restful-passing-parameters-to-get-request

# v1 hard code queries (this)
# future v2 use SQLalchemy ORM
# future v3 port to FastAPI w/ async/await

from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api
# from sqlalchemy import create_engine

from Helpers import *
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


#--- ALL UNIQUE ROUTES IN HISTORY (JSON)---#
class KnownRoutes(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("SELECT DISTINCT route_short FROM buses")
        results = {'routes': [i[0] for i in query.cursor.fetchall()]}
        return jsonify(results)

#--- ALL BUSES IN LAST 60 SECONDS FOR LIVE MAP (GEOJSON) ---#
class LiveMap(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM buses WHERE timestamp >= NOW() - INTERVAL 60 SECOND;") #todo refine this to smooth out
        results = {'observations': unpack_query_results(query)}
        geojson = results_to_FeatureCollection(results)
        return geojson




class TripQuerySchema(Schema):
    service_date = fields.Str(required=True)
    trip_id = fields.Str(required=True)
    output = fields.Str(required=True)

trip_schema = TripQuerySchema()

#--- ALL OBSERVATIONS FOR A SINGLE UNIQUE TRIP (GEOJSON) ---#

class TripAPI(Resource):
    def get(self):
        errors = trip_schema.validate(request.args)
        if errors:
            abort(400, str(errors))
        conn = db_connect.connect()
        query_suffix = query_builder(request.args)
        query = conn.execute("SELECT * FROM buses WHERE {}".format(query_suffix ))
        results = {'observations': unpack_query_results(query)}
        if request.args['output'] == 'geojson':
            return results_to_FeatureCollection(results)
        elif request.args['output'] == 'kepler':
            return results_to_KeplerTable(results)

#--- URLS ---#
api.add_resource(KnownRoutes, '/api/v1/nyc/knownroutes')
api.add_resource(LiveMap, '/api/v1/nyc/livemap')
api.add_resource(TripAPI, '/api/v1/nyc/trips', endpoint='trips')


if __name__ == '__main__':
    app.run(debug=True)