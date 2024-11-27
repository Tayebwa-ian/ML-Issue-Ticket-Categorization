#!/usr/bin/python3
"""API interface module for interacting with the AI model"""
from flask_restful import Resource
from flask import jsonify, make_response, request
from ..serializers.issue import IssueSchema 
from marshmallow import ValidationError, EXCLUDE
# from app import model
from ..utils.utils import data_preprocessor
from Storage.storage import Issue


issue_schema = IssueSchema(unknown=EXCLUDE)
issues_schema = IssueSchema(many=True)


class IssueList(Resource):
    """Implements requests to the model and to the database"""
    def get(self):
        """Testing server connection"""
        response = {
            "status": "success",
            "message": "connected to the server"
        }
        return make_response(jsonify(response), 200)
    
    def post(self):
        """retrieve information from the request object.
            ** pass the information to the model for prediction
            ** Post the prediction and information to the database
        """
        data = request.get_json()
        try:
            data = issue_schema.load(data)
            data = issue_schema.load(data)
        except ValidationError as e:
            responseobject = {
                "status": "fail",
                "message": e.messages
            }
            return make_response(jsonify(responseobject))
        #X = data_preprocessor(data)
        #prediction = model.predict(X) # make a prediction
        #data['prediction'] = prediction
        new_issue = Issue(**data)
        new_issue.save()

        return issue_schema.dump(new_issue), 201
