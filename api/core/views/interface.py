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
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST


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
        probabilities = model.predict_proba(X)
        pred_confidence = probabilities[0][0]  # get the prediction confidence
        # get the string equivalent
        prediction = interpret_prediction(prediction)

        data['prediction'] = prediction
        data['pred_confidence'] = pred_confidence
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


class Monitoring(Resource):
    """
    Setup metrics to monintor in this app using prometheus
    """
    def get(self):
        """returns all setup metrics"""
        return make_response(
            generate_latest(),
            200,
            {'Content-Type': CONTENT_TYPE_LATEST}
            )

    @staticmethod
    def compute_details() -> None:
        """
        Calculates the following metrics
            1. Accuracy
            2. Average prediction confidence
            3. Number of predictions per category
            4. Number of correct predictions per category
            5. Number of incorrect predictions per category
        """
        issues = storage.all(Issue)  # Query all issues from DB

        # Metrics
        accuracy = Gauge(
            'ticket_model_accuracy',
            'Model accuracy as a percentage')
        avg_pred_confidence = Gauge(
            'ticket_model_avg_pred_confidence',
            'Average prediction confidence')
        bug_pred = Gauge(
            'ticket_model_bug_pred',
            'Number of bug predictions')
        enhancement_pred = Gauge(
            'ticket_model_enhancement_pred',
            'Number of enhancement predictions')
        question_pred = Gauge(
            'ticket_model_question_pred',
            'Number of question predictions')
        correct_bug_pred = Gauge(
            'ticket_model_correct_bug_pred',
            'Number of correct bug predictions')
        incorrect_bug_pred = Gauge(
            'ticket_model_incorrect_bug_pred',
            'Number of incorrect bug predictions')
        correct_enhancement_pred = Gauge(
            'ticket_model_correct_enhancement_pred',
            'Number of correct enhancement predictions')
        incorrect_enhancement_pred = Gauge(
            'ticket_model_incorrect_enhancement_pred',
            'Number of incorrect enhancement predictions')
        correct_question_pred = Gauge(
            'ticket_model_correct_question_pred',
            'Number of correct question predictions')
        incorrect_question_pred = Gauge(
            'ticket_model_incorrect_question_pred',
            'Number of incorrect question predictions')
        data = {
            'accuracy': 0.0,
            'avg_pred_confidence': 0.0,
            'bug_pred': 0,
            'enhancement_pred': 0,
            'question_pred': 0,
            'correct_bug_pred': 0,
            'incorrect_bug_pred': 0,
            'correct_enhancement_pred': 0,
            'incorrect_enhancement_pred': 0,
            'correct_question_pred': 0,
            'incorrect_question_pred': 0,
        }

        for issue in issues:
            if issue.prediction == 'Bug':
                data['bug_pred'] += 1
                if issue.actual_label == 'Bug':
                    data['correct_bug_pred'] += 1
                else:
                    data['incorrect_bug_pred'] += 1
            elif issue.prediction == 'Enhancement':
                data['enhancement_pred'] += 1
                if issue.actual_label == 'Enhancement':
                    data['correct_enhancement_pred'] += 1
                else:
                    data['incorrect_enhancement_pred'] += 1
            elif issue.prediction == 'Question':
                data['question_pred'] += 1
                if issue.actual_label == 'Question':
                    data['correct_question_pred'] += 1
                else:
                    data['incorrect_question_pred'] += 1
        data['accuracy'] = (
            (data['correct_bug_pred'] +
             data['correct_enhancement_pred'] +
             data['correct_question_pred']) /
            len(issues)) * 100
        data['avg_pred_confidence'] = (sum([
            issue.pred_confidence for issue in issues
        ])) / len(issues)

        # Update Prometheus metrics
        accuracy.set(data["accuracy"])
        avg_pred_confidence.set(data["avg_pred_confidence"])
        bug_pred.set(data["bug_pred"])
        enhancement_pred.set(data["enhancement_pred"])
        question_pred.set(data["question_pred"])
        correct_bug_pred.set(data["correct_bug_pred"])
        incorrect_bug_pred.set(data["incorrect_bug_pred"])
        correct_enhancement_pred.set(data["correct_enhancement_pred"])
        incorrect_enhancement_pred.set(data["incorrect_enhancement_pred"])
        correct_question_pred.set(data["correct_question_pred"])
        incorrect_question_pred.set(data["incorrect_question_pred"])
