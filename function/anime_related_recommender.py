import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

@st.cache_data(show_spinner=False)
def compute_similarity(filtered_df):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(filtered_df['Genre'])
    return cosine_similarity(tfidf_matrix, tfidf_matrix)

def recommend(df, anime_title, result_count=6, filter_18=True, filter_rating=0.0):
    if filter_18:
        df_filtered_18 = df[~df['18+']].reset_index(drop=True)
    else:
        df_filtered_18 = df.reset_index(drop=True)

    df_filtered_rating = df_filtered_18[df_filtered_18['Rating'] >= filter_rating].reset_index(drop=True)

    if anime_title not in df_filtered_rating['Title'].values:
        anime_row = df[df['Title'] == anime_title]
        if not anime_row.empty:
            df_filtered_rating = pd.concat([df_filtered_rating, anime_row]).reset_index(drop=True)

    if anime_title not in df_filtered_rating['Title'].values:
        return pd.DataFrame()

    cosine_sim_filtered = compute_similarity(df_filtered_rating)
    idx = df_filtered_rating[df_filtered_rating['Title'] == anime_title].index[0]
    sim_scores = list(enumerate(cosine_sim_filtered[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:result_count+1]
    indices = [i[0] for i in sim_scores]
    
    return df_filtered_rating.iloc[indices][['Title','Genre','Rating','Link']].sort_values(by='Rating', ascending=False)
