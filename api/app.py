#!/usr/bin/python3
"""Application intialisation module"""

from flask import Flask
from os import getenv
from flask import Flask, jsonify, make_response
from flask_restful import Api
import joblib


# create the app instance
app = Flask(__name__)
# load the model
# model = joblib.load('random_forest_model.pkl')
api = Api(app)

from .core.views.interface import IssueList

api.add_resource(IssueList, '/status')

@app.errorhandler(404)
def page_not_found(e):
    """json 404 page"""
    return make_response(jsonify({"error": "Resource (enpoint Not) found"}), 404)

# run this file to run the app
if __name__ == "__main__":
    host = getenv("HH_API_HOST", "0.0.0.0")
    port = int(getenv("HH_API_PORT", "5000"))
    app.run(host, port=port, threaded=True, debug=True)
