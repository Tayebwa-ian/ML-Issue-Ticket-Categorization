#!/usr/bin/python3
"""API interface module for interacting with the AI model"""
from flask_restful import Resource
from flask import jsonify, make_response, request
from ..serializers.issue import IssueSchema
from marshmallow import ValidationError, EXCLUDE
from ..utils.utils import data_preprocessor, interpret_prediction, load_model
from ...Storage.storage import Issue
from ...Storage import storage
import pandas as pd


# load the model
model = load_model()


issue_schema = IssueSchema(unknown=EXCLUDE)
issues_schema = IssueSchema(many=True)


class PredictList(Resource):
    """Implements requests to for model predictions
        and stores them in database
    """
    def get(self):
        """returns all issues that have been reported with relevant details"""
        issues = storage.all(Issue)
        if not issues:
            response = {
                "status": "error",
                "message": "could not fetch issues from the storage",
                "data": issues
            }
            return make_response(jsonify(response), 400)
        return issues_schema.dump(issues), 200

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

        # Match the data fields with those used in training
        raw_data = {
            "issue_title": data.get('title'),
            "issue_body": data.get('body'),
            "issue_author_association": data.get('author')
        }
        # Convert to DataFrame with an index
        # Specify the index explicitly
        prediction_data = pd.DataFrame([raw_data])
        X = data_preprocessor(prediction_data)

        prediction = model.predict(X)  # make a prediction
        prediction = interpret_prediction(prediction)

        data['prediction'] = prediction
        new_issue = Issue(**data)
        storage.new(new_issue)
        storage.save()

        return issue_schema.dump(new_issue), 201


class CorrectList(Resource):
    """Implements requests to correct model predictions"""
    def get(self, id):
        """Return information about a single issue
        Param:
            id: ID of the issue
        """
        issue = storage.get(Issue, id)
        if issue:
            return issue_schema.dump(issue), 200
        response = {
            "status": "fail",
            "message": f"Could not fetch issue with ID {id}",
            "data": issue
        }
        return make_response(jsonify(response), 401)

    def put(self, id):
        """
        captured the correct prediction and insert it in the database
        Param:
            id: ID of the issue to correct
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
        issue = storage.update(Issue, id, **data)
        return issue_schema.dump(issue), 200
