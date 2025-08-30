import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def compute_weighted_rating(R, v, C, m):
    """Bayesian weighted rating formula"""
    return ((R * v) + (C * m)) / (v + m)

def recommend(df, anime_title, filter_18=False, filter_rating=0.0):
    # 基础过滤 (18+ / rating)
    from data.data_filter import data_filter
    df_filtered = data_filter(df, anime_title, filter_18, filter_rating)

    # 找出选中的 anime
    anime_row = df[df['Title'] == anime_title]
    if anime_row.empty:
        return pd.DataFrame(), pd.DataFrame()

    # 选中 anime 的 genres (可能有多个, 逗号分隔 / 空格分隔)
    target_genres = str(anime_row.iloc[0]['Genre']).split()
    # 可以改成 split(",") 如果你的 Genre 是 "Music, Drama" 这种格式

    # 过滤掉不含相同 genre 的 anime
    mask = df_filtered['Genre'].apply(
        lambda g: any(tg.lower() in str(g).lower() for tg in target_genres)
    )
    df_filtered = df_filtered[mask]

    if df_filtered.empty:
        # 没有 genre 匹配，就返回原 anime info
        return pd.DataFrame(), anime_row[['Title', 'Genre', 'Rating', 'Link', 'Votes']]

    # 平均分 (全局 C) 和最少投票数 (m)
    C = df_filtered['Rating'].mean()
    m = 1000  # 你可以调节这个参数

    # 计算 Weighted Rating
    v = df_filtered['Votes']
    R = df_filtered['Rating']
    df_filtered = df_filtered.copy()
    df_filtered['WeightedRating'] = compute_weighted_rating(R, v, C, m)

    # 去掉自己
    df_filtered = df_filtered[df_filtered['Title'] != anime_title]

    # 排序
    recs_sorted = df_filtered.sort_values(by='WeightedRating', ascending=False)

    return recs_sorted[['Title', 'Genre', 'Rating', 'Link', 'WeightedRating', 'Votes']], \
           anime_row[['Title', 'Genre', 'Rating', 'Link', 'Votes']]
