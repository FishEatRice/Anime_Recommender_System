import streamlit as st
import pandas as pd
import numpy as np
import random
from sklearn.metrics import precision_score, recall_score, f1_score
from session.data_session import *
from data.data_loader import *
from sklearn.metrics.pairwise import cosine_similarity

st.title("Precision / Recall / F1")

session_state_format()
st.session_state.where_page = "value_page"
session_check_where()

df_animes, df_reviews = load_data()

def build_similarity(df_animes, df_reviews):
    reviews = df_reviews[['profile', 'anime_uid', 'rating']].dropna()
    animes = df_animes[['uid', 'title']]
    anime_map = dict(zip(animes['uid'].astype(str), animes['title']))
    reviews['title'] = reviews['anime_uid'].astype(str).map(anime_map)
    reviews = reviews.dropna(subset=['title'])
    reviews['rating'] = pd.to_numeric(reviews['rating'], errors='coerce')
    anime_user_matrix = reviews.pivot_table(
        index='title', columns='profile', values='rating'
    ).fillna(0)
    anime_similarity = cosine_similarity(anime_user_matrix)
    anime_similarity_df = pd.DataFrame(
        anime_similarity,
        index=anime_user_matrix.index,
        columns=anime_user_matrix.index
    )
    return anime_similarity_df, reviews

anime_similarity_df, reviews = build_similarity(df_animes, df_reviews)

random.seed(42)
np.random.seed(42)

def leave_one_out_split(reviews):
    train, test = [], []
    for user, group in reviews.groupby("profile"):
        if len(group) < 2:
            train.extend(group.to_dict("records"))
            continue
        test_idx = random.choice(range(len(group)))
        for i, row in enumerate(group.to_dict("records")):
            if i == test_idx:
                test.append(row)
            else:
                train.append(row)
    return pd.DataFrame(train), pd.DataFrame(test)

def get_recommendations(anime_title, similarity_df, top_n=10):
    if anime_title not in similarity_df.index:
        return []
    sim_scores = similarity_df[anime_title].sort_values(ascending=False)
    return sim_scores.index[1:top_n+1].tolist()

def evaluate(reviews, anime_similarity_df, threshold=7, top_n=10):
    train, test = leave_one_out_split(reviews)
    y_true, y_pred = [], []
    for user, group in test.groupby("profile"):
        liked_animes = set(group[group["rating"] >= threshold]["title"])
        if not liked_animes:
            continue
        user_train_likes = train[(train["profile"] == user) & (train["rating"] >= threshold)]["title"].tolist()
        if not user_train_likes:
            continue
        recommended = set()
        for anime in user_train_likes:
            recommended.update(get_recommendations(anime, anime_similarity_df, top_n=top_n))
        for anime in liked_animes:
            y_true.append(1)
            y_pred.append(1 if anime in recommended else 0)

    if not y_true: 
        return 0.0, 0.0, 0.0

    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    return precision, recall, f1

with st.spinner("Processing... This may take a while."):
    precision, recall, f1 = evaluate(reviews, anime_similarity_df)

st.success("Done!") 

st.metric("Precision", f"{precision:.3f}")
st.write(f"- **Precision {precision:.3f}** → The recommendations are very accurate (almost no irrelevant items).")

st.markdown("<br>", unsafe_allow_html=True)

st.metric("Recall", f"{recall:.3f}")
st.write(f"- **Recall {recall:.3f}** → Only about {recall*100:.1f}% of the items the user actually likes were retrieved, meaning many were missed.")

st.markdown("<br>", unsafe_allow_html=True)

st.metric("F1", f"{f1:.3f}")
st.write(f"- **F1 {f1:.3f}** → The overall balance is modest, mainly because recall is low.")