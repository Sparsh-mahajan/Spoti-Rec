import get_features
import get_recommendations
import pandas as pd
import os

playlist_link = "https://open.spotify.com/playlist/37i9dQZF1E8Hir1avHtgPH?si=30f0526211bf4694"
src_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(os.path.abspath(src_dir))
data_dir = os.path.join(project_dir, "data")
playlist_df = get_features.get_playlist_features(playlist_link)
database_df = pd.read_csv(os.path.join(data_dir, "database_df.csv"))
features_df = pd.read_csv(os.path.join(data_dir, "final_features.csv"))
rec_df = get_recommendations.recommend(playlist_df, features_df, database_df)
