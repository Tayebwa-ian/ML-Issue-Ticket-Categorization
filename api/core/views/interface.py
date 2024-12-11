#!/usr/bin/python3
"""API interface module for interacting with the AI model"""
from flask_restful import Resource
from flask import jsonify, make_response, request
from ..serializers.issue import IssueSchema
from marshmallow import ValidationError, EXCLUDE
from ..utils.utils import data_preprocessor, interpret_prediction, load_model
from ...Storage.storage import Issue


# load the model
model = load_model()


issue_schema = IssueSchema(unknown=EXCLUDE)
issues_schema = IssueSchema(many=True)


class PredictList(Resource):
    """Implements requests to for model predictions
        and stores them in database
    """
    def get(self):
        """connection prediction endpoint"""
        response = {
            "status": "success",
            "message": "connection to prediction endpoint is successful"
        }
        return make_response(jsonify(response), 200)

    def post(self):
        """retrieve information from the request object.
            ** pass the information to the model for prediction
            ** Post the prediction and information to the database
        Return: the predicted value and the issue ID
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
            return make_response(jsonify(responseobject), 403)
        X = data_preprocessor(data)
        prediction = model.predict(X)  # make a prediction
        prediction = interpret_prediction(prediction)
        data['prediction'] = prediction
        new_issue = Issue(**data)
        new_issue.save()

        return issue_schema.dump(new_issue), 201


class CorrectList(Resource):
    """Implements requests to correct model predictions"""
    def get(self, id):
        """correction endpoint connection"""
        response = {
            "status": "success",
            "message": "connection to correction endpoint is successful"
        }
        return make_response(jsonify(response), 200)

    def put(self, id):
        """
        captured the correct prediction and insert it in the database
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
            return make_response(jsonify(responseobject), 403)
        issue = Issue.update(id, **data)
        return issue_schema.dump(issue), 200
