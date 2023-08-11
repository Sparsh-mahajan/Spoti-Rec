import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id='9aa01b97021549f29427a140483c7759',client_secret='36b5fd231e5249ad9d4a4205451d87ce')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_playlist_features(playlist_uri):
    playlist_data = sp.playlist_items(playlist_uri)

    playlist_tracks_names = []
    playlist_tracks_ids = []
    playlist_tracks_artists = []
    playlist_tracks_first_artists = []

    for track in playlist_data["items"]:
        playlist_tracks_ids.append(track["track"]["id"])
        playlist_tracks_names.append(track["track"]["name"])
        artist_list = []
        for artist in track["track"]["artists"]:
            artist_list.append(artist)
        playlist_tracks_artists.append(artist_list)
        playlist_tracks_first_artists.append(artist_list[0])

    features = sp.audio_features(playlist_tracks_ids)
    features_df = pd.DataFrame(data=features, columns=features[0].keys())

    features_df["title"] = playlist_tracks_names
    features_df["first_artist"] = playlist_tracks_first_artists
    features_df["all_artists"] = playlist_tracks_artists

    features_df = features_df[['id', 'title', 'first_artist', 'all_artists',
                               'danceability', 'energy', 'key', 'loudness',
                               'mode', 'acousticness', 'instrumentalness',
                               'liveness', 'valence', 'tempo',
                               'duration_ms', 'time_signature']]
    return features_df
