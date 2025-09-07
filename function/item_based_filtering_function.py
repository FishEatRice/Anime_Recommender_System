import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def item_based_filtering_recommend(df_animes, df_reviews, selected_anime):
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
    df_reviews_matrix = df_reviews.pivot_table(
        index='anime_uid', 
        columns='profile', 
        values='rating'
    ).fillna(0)

    if selected_anime_uid not in df_reviews_matrix.index:
        return pd.DataFrame(), pd.DataFrame()
    
    # Compute cosine similarity between animes
    cosine_animes_similarity = cosine_similarity(df_reviews_matrix)
    df_cosine_animes_similarity = pd.DataFrame(
        cosine_animes_similarity,
        index=df_reviews_matrix.index,
        columns=df_reviews_matrix.index
    )
    
    # Get similarity scores for the selected anime
    sim_scores = df_cosine_animes_similarity[selected_anime_uid]
    sim_scores = sim_scores.drop(selected_anime_uid)

    # Filter available columns for recommendations
    available_cols = ['uid','title', 'genre', 'score', 'synopsis', 'link', 'similarity']
    available_cols = [c for c in available_cols if c in df_animes.columns]

    # Merge the similarity scores with anime details
    recommend_result = df_animes[available_cols].drop_duplicates(subset="title")

    # Map similarity scores to the anime UID column
    recommend_result['similarity'] = recommend_result['uid'].map(sim_scores)

    recommend_result = recommend_result.dropna(subset=['similarity'])

    # Sort by similarity
    recommend_result = recommend_result.sort_values(by='similarity', ascending=False)

    return recommend_result, selected_anime_details
