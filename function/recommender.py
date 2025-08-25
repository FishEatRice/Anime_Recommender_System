import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

@st.cache_data(show_spinner=False)
def compute_similarity(filtered_df):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(filtered_df['Genre'])
    return cosine_similarity(tfidf_matrix, tfidf_matrix)

def recommend(df, anime_title, top_n=6, filter_hentai=True):
    if filter_hentai:
        df_filtered = df[~df['Genre'].str.contains("Hentai", case=False, na=False)].reset_index(drop=True)
    else:
        df_filtered = df.reset_index(drop=True)

    if anime_title not in df_filtered['Title'].values:
        return pd.DataFrame()

    cosine_sim_filtered = compute_similarity(df_filtered)
    idx = df_filtered[df_filtered['Title'] == anime_title].index[0]
    sim_scores = list(enumerate(cosine_sim_filtered[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    indices = [i[0] for i in sim_scores]
    return df_filtered.iloc[indices][['Title','Genre','Rating','Link']].sort_values(by='Rating', ascending=False)

def recommend_by_keyword(df, keyword, top_n=6, filter_hentai=True):
    if filter_hentai:
        filtered_df = df[~df['Genre'].str.contains("Hentai", case=False, na=False)]
    else:
        filtered_df = df

    filtered_df = filtered_df[filtered_df['Genre'].str.contains(keyword, case=False, na=False)]
    return filtered_df[['Title','Genre','Rating','Link']].sort_values(by='Rating', ascending=False).head(top_n)
