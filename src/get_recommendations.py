from sklearn.metrics.pairwise import cosine_similarity


def generate_playlist_feature_vec(playlist_df, features_df):
    playlist_features = features_df[features_df["id"].isin(playlist_df["id"].values)]
    non_playlist_features = features_df[~(features_df["id"].isin(playlist_df["id"].values))]
    playlist_feature_vec = playlist_features.drop(columns="id").sum(axis=0)
    return playlist_feature_vec, non_playlist_features


def generate_recommendation(playlist_feature_vec, non_playlist_features, database_df):
    non_playlist_df = database_df[database_df["id"].isin(non_playlist_features["id"])].copy()
    non_playlist_df.loc[:, "similarity_score"] = cosine_similarity(non_playlist_features.drop(columns="id"),
                                                            playlist_feature_vec.values.reshape(1, -1))
    top_40_recommendation = non_playlist_df.sort_values("similarity_score", ascending=False).head(40)
    return top_40_recommendation


def recommend(playlist_df, features_df, database_df):
    playlist_feature_vec, non_playlist_features = generate_playlist_feature_vec(playlist_df, features_df)
    top_40_songs_df = generate_recommendation(playlist_feature_vec, non_playlist_features, database_df)
    return top_40_songs_df
