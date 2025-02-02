#!/usr/bin/python3
"""Issue schema module"""
from marshmallow import Schema, fields, validates, ValidationError
from langdetect import detect


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

    # @validates('title')
    # def validate_title(self, value) -> None:
    #     """Validate if the title field is in english
    #     Params:
    #         value: the input value
    #     """
    #     word = self.truncate_to_three_words(value)
    #     try:
    #         lang = detect(value)
    #     except Exception as e:
    #         raise ValidationError(
    #             f'Error: {e}'
    #         )
    #     if lang != 'en':
    #         raise ValidationError(
    #             f'{value} is not a valid English sentence'
    #         )

    # def truncate_to_three_words(self, sentence):
    #     """Truncates a sentence to the first three words.

    #     Args:
    #         sentence: The input sentence (string).

    #     Returns:
    #         The first three words of the sentence, or the original sentence
    #         if it has fewer than three words.  Returns an empty string if the
    #         input sentence is empty or None.
    #     """
    #     if not sentence: # Check for empty string or None input
    #         return ""

    #     words = sentence.split()
    #     return " ".join(words[:3])  # Join the first 3 words (or fewer)
