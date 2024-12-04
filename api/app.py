#!/usr/bin/python3
"""Application intialisation module"""

from flask import Flask
from os import getenv
from flask import Flask, jsonify, make_response
from .Storage import storage
from flask_restful import Api


# create the app instance
app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    """json 404 page"""
    return make_response(jsonify({"error": "Resource (endpoint Not) found"}), 404)

@app.teardown_appcontext
def teardown(self) -> None:
    """Close the storage session"""
    storage.close()

@app.errorhandler(400)
def handle_bad_request(e):
    """json 400 page"""
    return (jsonify({'error': 'Bad request'}))

# setup the API and the endpoints
api = Api(app)
from .core.views.interface import *

api.add_resource(PredictList, '/api/predict')

# run this file to run the app
if __name__ == "__main__":
    host = getenv("TICKET_API_HOST", "0.0.0.0")
    port = int(getenv("TICKET_API_PORT", "5000"))
    app.run(host, port=port, threaded=True, debug=True)
