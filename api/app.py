#!/usr/bin/python3
"""Application intialisation module"""

from flask import Flask
from os import getenv
from flask_restful import Api


# create the app instance
app = Flask(__name__)
# creation of API instance with the flask app instance
api = Api(app)

from views.interface import *
# register urls to the resource
api.add_resource(Issues, '/connect')

# run this file to run the app
if __name__ == "__main__":
    host = getenv("HH_API_HOST", "0.0.0.0")
    port = int(getenv("HH_API_PORT", "5000"))
    app.run(host, port=port, threaded=True, debug=True)
