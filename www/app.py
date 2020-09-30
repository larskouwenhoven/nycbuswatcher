import os

# https://bootstrap-flask.readthedocs.io/en/stable/
from flask_bootstrap import Bootstrap
from flask import Flask

app = Flask(__name__)

bootstrap = Bootstrap(app)

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("MAPBOX_API_KEY")
api_url_stem="/api/v1/nyc/livemap"

@app.route('/')
def index():
    return 'Index Page'


if __name__ == '__main__':
    app.run(debug=True)

# https://docs.mapbox.com/mapbox-gl-js/api/
## add to head

# <script src='https://api.mapbox.com/mapbox-gl-js/v1.12.0/mapbox-gl.js'></script>
# <link href='https://api.mapbox.com/mapbox-gl-js/v1.12.0/mapbox-gl.css' rel='stylesheet' />

## add to body

# <div id='map' style='width: 400px; height: 300px;'></div>
# <script>
# // TO MAKE THE MAP APPEAR YOU MUST
# // ADD YOUR ACCESS TOKEN FROM
# // https://account.mapbox.com
# mapboxgl.accessToken = '<your access token here>';
# var map = new mapboxgl.Map({
#     container: 'map',
#     style: 'mapbox://styles/mapbox/streets-v11', // stylesheet location
#     center: [-74.5, 40], // starting position [lng, lat]
#     zoom: 9 // starting zoom
# });
# </script>

