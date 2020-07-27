import json
from flask import Blueprint, request, jsonify, render_template, Flask
from flask_cors import CORS, cross_origin
import pandas as pd
import joblib
import os
import requests

# # *************************************************************************** #
# # Activating CORS
# app = Flask(__name__)
# app.config['CORS_HEADERS'] = 'Content-Type'
# cors = CORS(app)
# # *************************************************************************** #

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

# @api_routes.route('/send', methods = ["POST"])
@api_routes.route('/send')
# @cross_origin()
def process_json():
    sent_track_id = '3J2Jpw61sO7l6Hc7qdYV91'
    print('Fetching payload')
    # pyld = request.get_json()
    print(f'Payload: {sent_track_id}')

    # print('processig and recommending basd on payload')
    # preprocessed = clean_payload(pyld)
    #
    #
    # print('Preparing response')
    # clean_recs = clean_response(recs, pyld['UserID'])
    #
    # print('Sending response')
    #
    # response = app.response_class(
    #     json.dumps(clean_recs, sort_keys=False, indent=4),
    #     mimetype=app.config['JSONIFY_MIMETYPE']
    # )
    return sent_track_id

@api_routes.route('/')
def hello_world():
    return 'Hello, World!'