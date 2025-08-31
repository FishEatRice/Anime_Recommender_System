import pandas as pd

def compute_weighted_rating(R, v, C, m):
    """Bayesian weighted rating formula"""
    return ((R * v) + (C * m)) / (v + m)

def recommend(df, anime_title, filter_18=False, filter_rating=0.0):
    from data.data_filter import data_filter
    df_filtered = data_filter(df, anime_title, filter_18, filter_rating)

    # 找出选中的 anime
    anime_row = df[df['Title'] == anime_title]
    if anime_row.empty:
        return pd.DataFrame(), pd.DataFrame()

    # 目标 anime 的 genres (多个)
    target_genres = set(str(anime_row.iloc[0]['Genre']).replace(",", " ").split())

    # 计算每个候选和目标的 genre 相似度 (交集 / 并集, Jaccard similarity)
    def genre_similarity(genres):
        genres_set = set(str(genres).replace(",", " ").split())
        if not genres_set:
            return 0
        return len(target_genres & genres_set) / len(target_genres | genres_set)

    df_filtered = df_filtered.copy()
    df_filtered['GenreSim'] = df_filtered['Genre'].apply(genre_similarity)

    # 只保留 genre 有交集的 anime
    df_filtered = df_filtered[df_filtered['GenreSim'] > 0]

    if df_filtered.empty:
        return pd.DataFrame(), anime_row[['Title','Genre','Rating','Link','Votes']]

    # 全局平均分和投票阈值
    C = df_filtered['Rating'].mean()
    m = 1000  

    # Weighted Rating
    v = df_filtered['Votes']
    R = df_filtered['Rating']
    df_filtered['WeightedRating'] = compute_weighted_rating(R, v, C, m)

    # 自己要排除
    df_filtered = df_filtered[df_filtered['Title'] != anime_title]

    # 混合分数 = α * Genre 相似度 + (1-α) * Weighted Rating (归一化后)
    # 先归一化 WR
    wr_min, wr_max = df_filtered['WeightedRating'].min(), df_filtered['WeightedRating'].max()
    df_filtered['WRNorm'] = (df_filtered['WeightedRating'] - wr_min) / (wr_max - wr_min + 1e-9)

    alpha = 0.7  # genre 相似度权重更高
    df_filtered['HybridScore'] = alpha * df_filtered['GenreSim'] + (1-alpha) * df_filtered['WRNorm']

    # 排序
    recs_sorted = df_filtered.sort_values(by='HybridScore', ascending=False)

    return recs_sorted[['Title', 'Genre', 'Rating', 'Link', 'WeightedRating', 'Votes', 'GenreSim', 'HybridScore']], \
           anime_row[['Title','Genre','Rating','Link','Votes']]
