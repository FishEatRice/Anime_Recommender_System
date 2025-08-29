import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
from data.data_filter import data_filter

@st.cache_data(show_spinner=False)
def compute_similarity(filtered_df):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(filtered_df['Genre'])
    return cosine_similarity(tfidf_matrix, tfidf_matrix)

def recommend(df, anime_title, result_count=6, filter_18=False, filter_rating=0.0):
 
    df_filtered = data_filter(df, anime_title, filter_18, filter_rating)

    if anime_title not in df_filtered['Title'].values:
        anime_row = df[df['Title'] == anime_title]
        if not anime_row.empty:
            df_filtered = pd.concat([df_filtered, anime_row]).reset_index(drop=True)

    if anime_title not in df_filtered['Title'].values:
        return pd.DataFrame(), pd.DataFrame()

    cosine_sim_filtered = compute_similarity(df_filtered)
    idx = df_filtered[df_filtered['Title'] == anime_title].index[0]
    sim_scores = list(enumerate(cosine_sim_filtered[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:result_count+1]
    indices = [i[0] for i in sim_scores]

    df_filtered.shape
    
    # Calculate global average and threshold
    C = df_filtered['Rating'].mean()
    m = df_filtered['Votes'].quantile(0.30)

    recs = df_filtered.iloc[indices].copy()

    # Filter out low-vote animes (less than m)
    recs = recs[recs['Votes'] >= 1]  # Optional filter for realism

    v = recs['Votes']
    R = recs['Rating']
    recs['WeightedRating'] = (v / (v + m)) * R + (m / (v + m)) * C

    # Sort by weighted score
    recs = recs.sort_values(by='WeightedRating', ascending=False)


    return recs[['Title','Genre','Rating','Link','WeightedRating','Votes']].sort_values(by='WeightedRating', ascending=False), df_filtered.iloc[[idx]][['Title', 'Genre', 'Rating', 'Link', 'Votes']]
