import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit as st

@st.cache_data
def load_data(animes_path="data/animes.csv", reviews_path="data/reviews.csv"):
    df_animes = pd.read_csv(animes_path, encoding="utf-8")
    df_reviews = pd.read_csv(reviews_path, encoding="ISO-8859-1")

    df_animes = df_animes[['uid', 'title', 'genre', 'synopsis', 'score', 'link']].dropna()
    df_reviews = df_reviews[['profile', 'anime_uid', 'rating']].dropna()

    return df_animes, df_reviews
    
@st.cache_data
def get_anime_picture(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        img_tag = soup.find("img", {"itemprop": "image"})

        if img_tag:
            return img_tag.get("data-src") or img_tag.get("src")
        else:
            return "picture/picture_not_found.jpg"
    except Exception:
        return "picture/picture_not_found.jpg"