import os

# https://bootstrap-flask.readthedocs.io/en/stable/
from flask import Flask, render_template

app = Flask(__name__)


from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("MAPBOX_API_KEY")
api_url_stem="/api/v1/nyc/livemap"

@app.route('/')
def index():
    return render_template('index.html', title='NYCBusWatcher')

@app.route('/map')
def map():
    return render_template('map.html', title='NYCBusWatcher')


if __name__ == '__main__':
    app.run(debug=True)
