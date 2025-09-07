import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def user_based_filtering_recommend(df_animes, df_reviews, selected_anime):
    # Ensure proper numeric conversion for ratings and anime_uid
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
    df_reviews['anime_uid'] = pd.to_numeric(df_reviews['anime_uid'], errors='coerce')
    df_reviews['rating'] = df_reviews['rating'].fillna(0)

    # Find the selected anime details
    selected_anime_details = df_animes[df_animes['title'] == selected_anime]
    selected_anime_uid = selected_anime_details['uid'].values[0]
    selected_anime_details = selected_anime_details.drop_duplicates(subset="title")

    # Create a user-item matrix
    df_user_matrix = df_reviews.pivot_table(
        index='profile', 
        columns='anime_uid', 
        values='rating'
    ).fillna(0)

    # Compute cosine similarity between animes
    cosine_users_similarity = cosine_similarity(df_user_matrix)
    df_cosine_users_similarity = pd.DataFrame(
        cosine_users_similarity,
        index=df_user_matrix.index,
        columns=df_user_matrix.index
    )

    target_users = df_reviews[df_reviews['anime_uid'] == selected_anime_uid]['profile'].unique()
    if len(target_users) == 0:
        return "No users rated this anime", selected_anime_details
    
    target_user_self = target_users[0]

    if target_user_self not in df_cosine_users_similarity.columns:
        return "No user rated this anime", selected_anime_details
    
    sim_scores = df_cosine_users_similarity[target_user_self].sort_values(ascending=False)
    sim_scores = sim_scores.drop(target_user_self)

    neighbor_ratings = df_reviews[df_reviews['profile'].isin(sim_scores.index)]
    avg_ratings = neighbor_ratings.groupby('anime_uid')['rating'].mean()

    watched = df_reviews[df_reviews['profile'] == target_user_self]['anime_uid']
    avg_ratings = avg_ratings.drop(watched, errors='ignore')

    available_cols = ['uid','title','genre','score','synopsis','link']
    available_cols = [c for c in available_cols if c in df_animes.columns]

    recommend_result = df_animes[df_animes['uid'].isin(avg_ratings.index)][available_cols].drop_duplicates(subset="title")
    recommend_result['predicted_score'] = recommend_result['uid'].map(avg_ratings)

    recommend_result = recommend_result.sort_values(by='predicted_score', ascending=False)

    return recommend_result, selected_anime_details
