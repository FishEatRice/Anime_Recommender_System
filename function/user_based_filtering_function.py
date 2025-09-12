import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def user_based_filtering_recommend(df_animes, df_reviews, selected_animes, top_k=20):
    if isinstance(selected_animes, str):
        selected_animes = [selected_animes]

    all_recommendations = []
    all_selected_details = []

    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
    df_reviews['anime_uid'] = pd.to_numeric(df_reviews['anime_uid'], errors='coerce')
    df_reviews['rating'] = df_reviews['rating'].fillna(0)

    df_user_matrix = df_reviews.pivot_table(
        index='profile', 
        columns='anime_uid', 
        values='rating'
    ).fillna(0)

    cosine_users_similarity = cosine_similarity(df_user_matrix)
    df_cosine_users_similarity = pd.DataFrame(
        cosine_users_similarity,
        index=df_user_matrix.index,
        columns=df_user_matrix.index
    )

    for selected_anime in selected_animes:
        selected_anime_details = df_animes[df_animes['title'] == selected_anime]
        if selected_anime_details.empty:
            continue

        selected_anime_uid = selected_anime_details['uid'].values[0]
        all_selected_details.append(selected_anime_details)

        if selected_anime_uid not in df_user_matrix.columns:
            continue

        target_users = df_reviews[df_reviews['anime_uid'] == selected_anime_uid]['profile'].unique()
        if len(target_users) == 0:
            continue

        all_weighted_scores = []

        for target_user in target_users:
            if target_user not in df_cosine_users_similarity.index:
                continue

            sim_scores = df_cosine_users_similarity[target_user].drop(target_user)
            top_neighbors = sim_scores.sort_values(ascending=False).head(top_k)
            if top_neighbors.empty:
                continue

            neighbor_ratings = df_user_matrix.loc[top_neighbors.index]
            weighted_scores = (neighbor_ratings.T.dot(top_neighbors)) / top_neighbors.sum()
            weighted_scores = weighted_scores.dropna()

            watched = df_reviews[df_reviews['profile'] == target_user]['anime_uid'].unique()
            weighted_scores = weighted_scores.drop(watched, errors='ignore')

            all_weighted_scores.append(weighted_scores)

        if not all_weighted_scores:
            continue

        final_scores = pd.concat(all_weighted_scores, axis=1).mean(axis=1)

        available_cols = ['uid', 'title', 'genre', 'score', 'synopsis', 'link']
        available_cols = [c for c in available_cols if c in df_animes.columns]

        recommend_result = df_animes[df_animes['uid'].isin(final_scores.index)][available_cols].drop_duplicates(subset="title")
        recommend_result['predicted_score'] = recommend_result['uid'].map(final_scores)
        recommend_result = recommend_result.sort_values(by='predicted_score', ascending=False)

        all_recommendations.append(recommend_result)

    if all_recommendations:
        final_recommendations = all_recommendations[0]
        for rec in all_recommendations[1:]:
            final_recommendations = final_recommendations.merge(
                rec,
                on=['uid', 'title', 'genre', 'score', 'synopsis', 'link'],
                suffixes=("", "_y")
            )
            final_recommendations['predicted_score'] = final_recommendations[['predicted_score', 'predicted_score_y']].min(axis=1)
            final_recommendations = final_recommendations.drop(columns=['predicted_score_y'])

        final_recommendations = final_recommendations.sort_values(by="predicted_score", ascending=False)
    else:
        final_recommendations = pd.DataFrame()

    if all_selected_details:
        all_selected_details = pd.concat(all_selected_details).drop_duplicates(subset="uid")
    else:
        all_selected_details = pd.DataFrame()

    return final_recommendations, all_selected_details
