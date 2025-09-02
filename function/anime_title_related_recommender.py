import pandas as pd

def compute_weighted_rating(R, v, C, m):
    # Bayesian weighted rating formula
    return ((R * v) + (C * m)) / (v + m)

def recommend(df, anime_title, filter_18=False, filter_rating=0.0):
    from data.data_filter import data_filter
    df_filtered = data_filter(df, anime_title, filter_18, filter_rating)

    # Find Anime that selected
    anime_row = df[df['Title'] == anime_title]
    if anime_row.empty:
        return pd.DataFrame(), pd.DataFrame()

    # Taking Anime Genre
    target_genres = set(str(anime_row.iloc[0]['Genre']).replace(",", " ").split())

    # Calcalute similarity for each (Using Genre to calculate)
    def genre_similarity(genres):
        genres_set = set(str(genres).replace(",", " ").split())
        if not genres_set:
            return 0
        return len(target_genres & genres_set) / len(target_genres | genres_set)

    df_filtered = df_filtered.copy()
    df_filtered['GenreSim'] = df_filtered['Genre'].apply(genre_similarity)

    # Only Keep anime having high similarity (If not same genre, remove it)
    df_filtered = df_filtered[df_filtered['GenreSim'] > 0]

    if df_filtered.empty:
        return pd.DataFrame(), anime_row[['Title','Genre','Rating','Link','Votes']]

    # Calculate Weighted Rating
    C = df_filtered['Rating'].mean()
    m = 1000  

    # Weighted Rating
    v = df_filtered['Votes']
    R = df_filtered['Rating']
    df_filtered['WeightedRating'] = compute_weighted_rating(R, v, C, m)

    # Remove selected anime
    df_filtered = df_filtered[df_filtered['Title'] != anime_title]

    wr_min, wr_max = df_filtered['WeightedRating'].min(), df_filtered['WeightedRating'].max()
    df_filtered['WRNorm'] = (df_filtered['WeightedRating'] - wr_min) / (wr_max - wr_min + 1e-9)

    alpha = 0.7
    df_filtered['HybridScore'] = alpha * df_filtered['GenreSim'] + (1-alpha) * df_filtered['WRNorm']

    # Softing high to low
    recs_sorted = df_filtered.sort_values(by='HybridScore', ascending=False)

    # return Result + Selected
    return recs_sorted[['Title', 'Genre', 'Rating', 'Link', 'WeightedRating', 'Votes', 'GenreSim', 'HybridScore']], anime_row[['Title','Genre','Rating','Link','Votes']]
