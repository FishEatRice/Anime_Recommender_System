import pandas as pd

def compute_weighted_rating(R, v, C, m):
    return ((R * v) + (C * m)) / (v + m)

def recommend(df, selected_genres, filter_18=False, filter_rating=0.0):
    from data.data_filter import data_filter
    df_filtered = data_filter(df, None, filter_18, filter_rating)

    # Turn user input into a set
    target_genres = set(selected_genres)

    # Calculate similarity score against chosen genres
    def genre_similarity(genres):
        genres_set = set(str(genres).replace(",", " ").split())
        if not genres_set:
            return 0
        return len(target_genres & genres_set) / len(target_genres | genres_set)

    df_filtered = df_filtered.copy()
    df_filtered['GenreSim'] = df_filtered['Genre'].apply(genre_similarity)

    # Only keep anime with similarity > 0
    df_filtered = df_filtered[df_filtered['GenreSim'] > 0]

    if df_filtered.empty:
        return pd.DataFrame()

    # Weighted Rating
    C = df_filtered['Rating'].mean()
    m = 1000
    v = df_filtered['Votes']
    R = df_filtered['Rating']
    df_filtered['WeightedRating'] = compute_weighted_rating(R, v, C, m)

    # Normalize Weighted Rating
    wr_min, wr_max = df_filtered['WeightedRating'].min(), df_filtered['WeightedRating'].max()
    df_filtered['WRNorm'] = (df_filtered['WeightedRating'] - wr_min) / (wr_max - wr_min + 1e-9)

    # Hybrid score: combine genre similarity + weighted rating
    alpha = 0.7
    df_filtered['HybridScore'] = alpha * df_filtered['GenreSim'] + (1 - alpha) * df_filtered['WRNorm']

    # Sort descending
    recs_sorted = df_filtered.sort_values(by='HybridScore', ascending=False)

    return recs_sorted[['Title', 'Genre', 'Rating', 'Link', 'Votes', 'GenreSim', 'WeightedRating', 'HybridScore']]
