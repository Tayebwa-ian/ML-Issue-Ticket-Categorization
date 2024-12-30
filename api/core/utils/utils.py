
"""utility module"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
import joblib
import os
from scipy.sparse import hstack


def data_preprocessor(data):
    """
    Vectorization and feature engineering
    Arg:
        data: features from the raw data that are be be processed
    Return: preprocessed features into a single dataset
    """
    # Load pre-fitted transformers
    current_dir = os.path.dirname(__file__)
    title_v = os.path.join(current_dir, 'title_vectorizer.joblib')
    body_v = os.path.join(current_dir, 'body_vectorizer.joblib')
    enc = os.path.join(current_dir, 'encoder.joblib')
    title_vectorizer = joblib.load(title_v)
    body_vectorizer = joblib.load(body_v)
    encoder = joblib.load(enc)

    # Transform using pre-fitted vectorizers and encoder
    title = title_vectorizer.transform(data['issue_title'])
    body = body_vectorizer.transform(data['issue_body'])
    author = encoder.transform(data['issue_author_association'].to_frame())

    # creation of extra features that could improve the model
    data['issue_title_length'] = data['issue_title'].apply(len)
    data['issue_body_length'] = data['issue_body'].apply(len)
    error_words = ['error', 'bug']
    enhance_words = ['feature', 'update', 'enhance', 'add']
    data['possible_title_error'] = data['issue_title'].apply(
        lambda x: int(any(word in x.lower() for word in error_words)))
    data['possible_body_error'] = data['issue_body'].apply(
        lambda x: int(any(word in x.lower() for word in error_words)))
    data['possible_title_update'] = data['issue_title'].apply(
        lambda x: int(any(word in x.lower() for word in enhance_words)))
    data['possible_body_update'] = data['issue_body'].apply(
        lambda x: int(any(word in x.lower() for word in enhance_words)))

    # combine all the features
    X = hstack([author,
                title,
                body,
                data[['issue_title_length',
                      'issue_body_length',
                      'possible_title_error',
                      'possible_body_error',
                      'possible_title_update',
                      'possible_body_update',
                      ]].values
                ])

    return X


def interpret_prediction(prediction: int) -> str:
    """
    Takes the prediction as anumber
    returns the string equivalent of that number
    Params:
        prediction: the predictiopn value to change into a string
    Returns: A string representation of the prediction
    """
    if prediction == 0:
        return "Bug"
    elif prediction == 1:
        return "Enhancement"
    else:
        return "Question"


def load_model():
    """
    Simply load the ML model and return its instance
    """
    current_dir = os.path.dirname(__file__)
    model_path = os.path.join(current_dir, 'random_forest.pkl')

    return joblib.load(model_path)
