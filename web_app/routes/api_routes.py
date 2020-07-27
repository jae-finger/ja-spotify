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
    pickled_model = joblib.load(model_path)
    pickled_df = joblib.load(df_path)

    return (pickled_model, pickled_df)


PICKLED_MODEL, PICKLED_DF = load_models()


def lookup_song(track_id):
    """
    Takes in a sent track_id and returns the song info from pickled df
    :param track_id: track id from spotify db or relative
    :return: row + song information related to sent track_id
    """
    # liked_song = joblib.load('song_list.joblib')
    liked_song = PICKLED_DF[PICKLED_DF['track_id'] == track_id]
    return(liked_song)

def create_predicts(liked_song):
    """
    Function that returns k number of recommended songs. It returns row #s. The seed song (liked song) is the track_id sent via the JSON payload.
    :param liked_song: a returned df row pertaining to a user's liked song.
    :return: k rows of recommended songs as index numbers
    """
    liked_song = liked_song.drop(columns=['artist_name', 'track_id', 'track_name'])
    k_rec_songs = PICKLED_MODEL[1].kneighbors(PICKLED_MODEL[0].transform(liked_song))
    k_rec_songs = [k_rec_songs[1][0]]
    k_rec_songs = k_rec_songs[0][1:]
    return(k_rec_songs)

def deliver(song_list):
    """
    Takes in a list of 3 song indexes and returns a json of song info
    :param song_list: list of 3 track ids
    :return:
    """
    recommended_track_ids = []
    potential_songs = PICKLED_DF
    potential_songs = potential_songs[['artist_name', 'track_name', 'track_id']]
    for song in song_list:
        new_song = potential_songs.iloc[song]
        recommended_track_ids.append(new_song)
    recommended_track_ids = pd.DataFrame(recommended_track_ids)
    recommended_track_ids = recommended_track_ids[['track_id']]
    recommended_track_ids =  recommended_track_ids.to_json(orient='records')
    return recommended_track_ids


# @api_routes.route('/send', methods = ["POST"])
# @cross_origin()
@api_routes.route('/send')
def process_json():
    sent_track_id = '3J2Jpw61sO7l6Hc7qdYV91'
    print('Fetching payload')
    # pyld = request.get_json()
    print(f'Payload: {sent_track_id}')

    print('looking up song based on track id')
    wanted_song = lookup_song(sent_track_id)

    print('processing and recommending basd on payload')
    preds = create_predicts(wanted_song)
    print(preds)

    print('---------')
    print('Looking up predictions')
    del_payload = deliver(preds)
    print(del_payload)

    print('----------')
    print('Sending JSON')

    # response = app.response_class(
    #     json.dumps(del_payload, sort_keys=False, indent=4),
    #     mimetype=app.config['JSONIFY_MIMETYPE']
    # )
    # return response
    return f'{del_payload}'

@api_routes.route('/')
def hello_world():
    return 'hellllllllllo world'