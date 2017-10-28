'''
POI Map for Eugene, OR
'''

import flask
from flask import request
import config
import logging

app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page")
    return flask.render_template('map.html')

@app.errorhandler(404)
def page_note_found(error):
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html')

# AJAX requests

# Read our text file
@app.route("/_render_poi")
def _render_poi():
    poi_list = []
    # CONFIG.POI - location of txt file from credentials.ini
    pois = open(CONFIG.POI)
    # process file
    for line in pois:
        if len(line) == 0 or line[0] == "#":
            log.debug("Skip")
            continue
        parts = line.split(',')
        loc = (parts[0], parts[1], parts[2])
        poi_list.append(loc)
    app.logger.debug("poi_list= {}".format(poi_list))
    return flask.jsonify(result=poi_list)
    
####

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
 
