import json
from flask import Blueprint, request, jsonify, render_template, Flask
from flask_cors import CORS, cross_origin
import pandas as pd
import joblib
import os

api_routes = Blueprint("api_routes", __name__)

def safe_paths():
    '''
    Quick helper to make platform independant file paths
    Returns - (df, data)
    '''
    model_path = os.path.join('data',
                              'knn_pipeline.joblib')

    df_path = os.path.join('data',
                           'song_list.joblib')

    return (model_path, df_path)

def load_models():
    '''
    Helper function for loading pickled models
    '''
    model_path, df_path = safe_paths()

    # load the model from disk
    pickled_model = joblib.load('knn_pipeline.joblib')
    pickled_df = joblib.load('song_list.joblib')

    return (pickled_model, pickled_df)

@api_routes.route('/send', methods = ["POST"])