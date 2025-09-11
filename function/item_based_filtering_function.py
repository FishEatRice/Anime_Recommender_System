import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def item_based_filtering_recommend(df_animes, df_reviews, selected_animes):

    if isinstance(selected_animes, str):
        selected_animes = [selected_animes]

    all_recommendations = []
    all_selected_details = []

    for selected_anime in selected_animes:
        df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
        df_reviews['anime_uid'] = pd.to_numeric(df_reviews['anime_uid'], errors='coerce')
        df_reviews['rating'] = df_reviews['rating'].fillna(0)

        # Find anime details
        selected_anime_details = df_animes[df_animes['title'] == selected_anime]
        if selected_anime_details.empty:
            continue

        selected_anime_uid = selected_anime_details['uid'].values[0]
        all_selected_details.append(selected_anime_details)

        df_reviews_matrix = df_reviews.pivot_table(
            index='anime_uid',
            columns='profile',
            values='rating'
        ).fillna(0)

        if selected_anime_uid not in df_reviews_matrix.index:
            continue

        cosine_animes_similarity = cosine_similarity(df_reviews_matrix)
        df_cosine_animes_similarity = pd.DataFrame(
            cosine_animes_similarity,
            index=df_reviews_matrix.index,
            columns=df_reviews_matrix.index
        )

        sim_scores = df_cosine_animes_similarity[selected_anime_uid]
        sim_scores = sim_scores.drop(selected_anime_uid)

        available_cols = ['uid', 'title', 'genre', 'score', 'synopsis', 'link']
        available_cols = [c for c in available_cols if c in df_animes.columns]

        recommend_result = df_animes[available_cols].drop_duplicates(subset="title")
        recommend_result['similarity'] = recommend_result['uid'].map(sim_scores)
        recommend_result = recommend_result.dropna(subset=['similarity'])
        recommend_result = recommend_result.sort_values(by='similarity', ascending=False)

        all_recommendations.append(recommend_result)

    if all_recommendations:
        final_recommendations = all_recommendations[0]
        for rec in all_recommendations[1:]:
            # Only keep having same time items
            final_recommendations = final_recommendations.merge(
                rec,
                on=['uid', 'title', 'genre', 'score', 'synopsis', 'link'],
                suffixes=("", "_y")
            )

            # combine similarity 
            final_recommendations['similarity'] = (
                final_recommendations[['similarity', 'similarity_y']].min(axis=1)
            )
            final_recommendations = final_recommendations.drop(columns=['similarity_y'])

        final_recommendations = final_recommendations.sort_values(by="similarity", ascending=False)
    else:
        final_recommendations = pd.DataFrame()

    if all_selected_details:
        all_selected_details = pd.concat(all_selected_details).drop_duplicates(subset="uid")
    else:
        all_selected_details = pd.DataFrame()

    return final_recommendations, all_selected_details
