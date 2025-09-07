import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics.pairwise import cosine_similarity
from session.data_session import *
from data.data_loader import *

st.title("MSE & RMSE Evaluation")

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

def predict_rating(user, anime_title, train, similarity_df, k=5):
    user_ratings = train[train["profile"] == user]
    if user_ratings.empty or anime_title not in similarity_df.index:
        return np.nan

    sim_scores = similarity_df[anime_title].drop(anime_title, errors="ignore")
    sims, ratings = [], []
    for _, row in user_ratings.iterrows():
        title = row["title"]
        if title in sim_scores.index:
            sims.append(sim_scores[title])
            ratings.append(row["rating"])
    if not sims:
        return np.nan

    sims = np.array(sims)
    ratings = np.array(ratings)
    top_k_idx = np.argsort(sims)[-k:]
    sims = sims[top_k_idx]
    ratings = ratings[top_k_idx]

    if sims.sum() == 0:
        return np.nan
    return np.dot(sims, ratings) / sims.sum()

def evaluate_rmse(reviews, similarity_df, test_size=0.2):
    train, test = [], []
    for user, group in reviews.groupby("profile"):
        if len(group) < 2:
            train.extend(group.to_dict("records"))
            continue
        test_idx = np.random.choice(range(len(group)), size=max(1, int(len(group) * test_size)), replace=False)
        for i, row in enumerate(group.to_dict("records")):
            if i in test_idx:
                test.append(row)
            else:
                train.append(row)
    
    train = pd.DataFrame(train)
    test = pd.DataFrame(test)

    y_true, y_pred = [], []
    for _, row in test.iterrows():
        pred = predict_rating(row["profile"], row["title"], train, similarity_df)
        if not np.isnan(pred):
            y_true.append(row["rating"])
            y_pred.append(pred)

    if not y_true:
        return np.nan, np.nan

    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    return mse, rmse

with st.spinner("Calculating RMSE... This may take a while."):
    mse, rmse = evaluate_rmse(reviews, anime_similarity_df, test_size=0.2)

st.success("Done!")

st.write("### Interpretation")
if not np.isnan(mse) and not np.isnan(rmse):
    st.metric("MSE", f"{mse:.3f}")
    st.write(f"- **MSE {mse:.3f}** → On average, the squared error between predicted and actual ratings is {mse:.3f}. Lower is better.")

    st.markdown("<br>", unsafe_allow_html=True)

    st.metric("RMSE", f"{rmse:.3f}")
    st.write(f"- **RMSE {rmse:.3f}** → The average prediction error is about {rmse:.2f} rating points. "
             f"This means the system’s predictions are typically off by ~{rmse:.2f} on the rating scale.")

else:
    st.write("Not enough data to compute MSE/RMSE.")
