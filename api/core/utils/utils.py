
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

    # TF-IDF Vectorizers for title and body
    title_vectorizer = TfidfVectorizer(stop_words='english')
    body_vectorizer = TfidfVectorizer(stop_words='english')
    # Encode author association
    encoder = OneHotEncoder(sparse_output=False)

    title = title_vectorizer.fit_transform(data['issue_title'])
    body = body_vectorizer.fit_transform(data['issue_body'])
    author = encoder.fit_transform(data['issue_author_association'].to_frame())

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
