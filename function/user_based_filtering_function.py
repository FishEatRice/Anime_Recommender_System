import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def user_based_filtering_recommend(df_animes, df_reviews, selected_anime):
    # Ensure proper numeric conversion for ratings and anime_uid
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
    df_reviews['anime_uid'] = pd.to_numeric(df_reviews['anime_uid'], errors='coerce')
    df_reviews['rating'] = df_reviews['rating'].fillna(0)
    
    # Find the selected anime details
    selected_anime_details = df_animes[df_animes['title'] == selected_anime]
    if selected_anime_details.empty:
        return pd.DataFrame(), pd.DataFrame()

    selected_anime_uid = selected_anime_details['uid'].values[0]

    # Create a user-item matrix
    df_user_matrix = df_reviews.pivot_table(
        index='profile', 
        columns='anime_uid', 
        values='rating'
    ).fillna(0)

    if selected_anime_uid not in df_user_matrix.columns:
        return pd.DataFrame(), pd.DataFrame()

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
    
    all_weighted_scores = []

    # Find all user
    for target_user in target_users:
        if target_user not in df_cosine_users_similarity.index:
            continue

        # Find Top 20 User
        sim_scores = df_cosine_users_similarity[target_user].drop(target_user)
        top_neighbors = sim_scores.sort_values(ascending=False).head(20)

        if top_neighbors.empty:
            continue

        neighbor_ratings = df_user_matrix.loc[top_neighbors.index]

        weighted_scores = (neighbor_ratings.T.dot(top_neighbors)) / top_neighbors.sum()
        weighted_scores = weighted_scores.dropna()

        watched = df_reviews[df_reviews['profile'] == target_user]['anime_uid'].unique()
        weighted_scores = weighted_scores.drop(watched, errors='ignore')

        all_weighted_scores.append(weighted_scores)

    if not all_weighted_scores:
        return pd.DataFrame(), selected_anime_details

    final_scores = pd.concat(all_weighted_scores, axis=1).mean(axis=1)

    available_cols = ['uid','title','genre','score','synopsis','link']
    available_cols = [c for c in available_cols if c in df_animes.columns]

    recommend_result = df_animes[df_animes['uid'].isin(final_scores.index)][available_cols].drop_duplicates(subset="title")
    recommend_result['predicted_score'] = recommend_result['uid'].map(final_scores)

    recommend_result = recommend_result.sort_values(by='predicted_score', ascending=False)

    return recommend_result, selected_anime_details