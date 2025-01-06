#!/usr/bin/python3
"""Issue schema module"""
from marshmallow import Schema, fields


class IssueSchema(Schema):
    """Issue Schema for data serialization
    """
    id = fields.Str(dump_only=True)
    created_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)
    author = fields.Str(required=True)
    title = fields.Str(required=True)
    body = fields.Str(required=True)
    url = fields.Str()
    prediction = fields.Str()
    actual_label = fields.Str()
    pred_confidence = fields.Float()
