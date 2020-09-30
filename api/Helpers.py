from datetime import date, datetime

def unpack_query_results(query):
    return [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

def query_builder(parameters):
    query_suffix = ''
    for field, value in parameters.items():
        if field == 'output':
            pass
        else:
            query_suffix = query_suffix + '{} = "{}" AND '.format(field,value)
    query_suffix=query_suffix[:-4] # strip tailing ' AND'
    return query_suffix


# manually, per geoff boeing method
def results_to_FeatureCollection(results):
    geojson = {'type': 'FeatureCollection', 'features': []}
    for row in results['observations']:
        feature = {'type': 'Feature',
                   'properties': {},
                   'geometry': {'type': 'Point',
                                'coordinates': []}}
        feature['geometry']['coordinates'] = [row['lat'], row['lon']]
        for k, v in row.items():
            if isinstance(v, (datetime, date)):
                v = v.isoformat()
            print('k: {} v: {}'.format(k,v))
            feature['properties'][k] = v
        geojson['features'].append(feature)
    return geojson

## automated, with geojson library
# from geojson import Feature, Point, FeatureCollection
# def results_to_FeatureCollection(results):
#     my_feature = Feature(geometry=Point((1.6432, -19.123)))
#     my_other_feature = Feature(geometry=Point((-80.234, -22.532)))
#     return FeatureCollection([my_feature, my_other_feature])



def results_to_KeplerTable(query): # bug am i reversing the unpack_query_results process?
    fields = [{"name":x} for x in dict.keys(query[0])]
    rows = []
    for k,v in query.items():
        pass # todo unpack the query results into a list of lists
        rows.append('something',454.232,5454.3434)
    kepler_bundle = {"fields": fields, "rows": rows }
    return kepler_bundle
