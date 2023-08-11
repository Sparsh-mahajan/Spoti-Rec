from flask import Flask, session, request, redirect, render_template, url_for
from flask_session import Session
import spotipy
import pandas as pd
import os
import get_features
import get_recommendations
import sys
sys.path.append('..')
import config



# os.environ['SPOTIPY_CLIENT_ID']='9aa01b97021549f29427a140483c7759'
# os.environ['SPOTIPY_CLIENT_SECRET']='36b5fd231e5249ad9d4a4205451d87ce'
# os.environ['SPOTIPY_REDIRECT_URI']='http://127.0.0.1:8080'




scope = "playlist-modify-public"
src_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(os.path.abspath(src_dir))
data_dir = os.path.join(project_dir, "data")


app = Flask(__name__, static_folder=os.path.join(src_dir, "resources"))
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)


@app.route('/', methods=('GET', 'POST'))
def home():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(client_id='9aa01b97021549f29427a140483c7759',client_secret='36b5fd231e5249ad9d4a4205451d87ce',redirect_uri='http://127.0.0.1:8080',cache_handler=cache_handler, scope=scope, show_dialog=True)

    if request.args.get("code"):
        # Step 2. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        auth_url = auth_manager.get_authorize_url()
        return render_template('login.html', auth_url=auth_url)

    if request.method == "POST":
        playlist_link = request.form['playlist link']
        playlist_name = request.form['playlist name']

        playlist_uri = playlist_link.split('/')[-1].split('?')[0]

        return redirect(url_for('recommend', playlist_uri=playlist_uri, playlist_name=playlist_name))
    return render_template('home.html')


@app.route('/recommend/<string:playlist_uri>/<string:playlist_name>')
def recommend(playlist_uri, playlist_name):
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(client_id='9aa01b97021549f29427a140483c7759',client_secret='36b5fd231e5249ad9d4a4205451d87ce',redirect_uri='http://127.0.0.1:8080',cache_handler=cache_handler, scope=scope)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    playlist_df = get_features.get_playlist_features(playlist_uri)
    database_df = pd.read_csv(os.path.join(data_dir, "database_df.csv"))
    features_df = pd.read_csv(os.path.join(data_dir, "final_features.csv"))
    rec_df = get_recommendations.recommend(playlist_df, features_df, database_df)

    track_names = rec_df['track_name'].tolist()
    track_ids = rec_df['id']

    sp = spotipy.Spotify(auth_manager=auth_manager)
    user_id = sp.me()['id']
    playlist_id = sp.user_playlist_create(user=user_id, name=playlist_name)['id']
    sp.playlist_add_items(playlist_id=playlist_id, items=track_ids)

    return render_template('recommend.html', track_names=track_names, track_ids=track_ids, playlist_id=playlist_id)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
