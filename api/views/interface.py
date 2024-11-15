#!/usr/bin/python3
"""API interface module for interacting with the AI model"""
from flask_restful import Resource
from flask import jsonify, make_response


class Issues(Resource):
    """Implements requests to the model and to the database"""
    def get(self):
        """Testing server connection"""
        response = {
            "status": "success",
            "message": "connected to the server"
        }
        return make_response(jsonify(response), 200)
