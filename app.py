import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import requests
from bs4 import BeautifulSoup
from streamlit.commands.execution_control import rerun

@st.cache_data
def load_data():
    reviews = pd.read_csv("data/reviews.csv", encoding="ISO-8859-1")
    animes = pd.read_csv("data/animes.csv", encoding="utf-8")
    
    animes = animes[~animes['genre'].str.contains('Hentai', case=False, na=False)]
    animes = animes[['uid', 'title', 'genre', 'synopsis', 'score', 'link']].dropna()
    reviews = reviews[['profile', 'anime_uid', 'rating']].dropna()
    
    return animes, reviews

def session_state_format():
    if 'recommended_count' not in st.session_state:
        st.session_state.recommended_count = 9

    if 'title_recommender_result_page' not in st.session_state:
        st.session_state.title_recommender_result_page = 0

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

def display_title_based_recommendations():
    st.markdown("## Anime Selected")

    details = st.session_state.title_recommender_anime_select_details
    selected = details.iloc[0]
    title = selected['Title']
    link = selected['Link']
    rating = 0.0 if pd.isna(selected['Rating']) else selected['Rating']
    genre = selected['Genre']
    similarity_score = selected.get('Similarity', 0.0)

    if 'fast_search' not in st.session_state:
        st.session_state.fast_search = False

    if not st.session_state.fast_search:
        col3, col4 = st.columns([1, 3])
        with col3:
            img_url = get_anime_picture(link)
            st.image(img_url, width=150)
        with col4:
            st.markdown(f"[{title}]({link})")
            st.write(f"⭐ {rating:.2f} / 10.0")
            st.write(f"Similarity: {similarity_score:.3f}")
            cleaned_genre = str(genre).strip("[]").replace("'", "").strip()
            st.caption(cleaned_genre)

    st.markdown("---")

    per_page = st.session_state.get('recommended_count', 9)
    start = st.session_state.title_recommender_result_page * per_page
    end = start + per_page

    results = st.session_state.title_recommender_results
    page_results = results.iloc[start:end]

    st.markdown("## Recommended Anime")

    for row_start in range(0, len(page_results), 3):
        cols = st.columns(3)
        for col, (_, row) in zip(cols, page_results.iloc[row_start:row_start + 3].iterrows()):
            with col:
                if not st.session_state.fast_search:
                    img_url = get_anime_picture(row['Link'])
                    st.image(img_url, width=150)
                st.markdown(f"[{row['Title']}]({row['Link']})")
                similarity_score = row.get('Similarity', 0.0)
                st.write(f"⭐ {row['Rating']:.2f} / 10.0")
                st.write(f"Similarity: {similarity_score:.3f}")
                cleaned_genre = str(row['Genre']).strip("[]").replace("'", "").strip()
                st.caption(cleaned_genre)
        st.markdown("---")

    col5, col6, col7 = st.columns([1, 2, 1])
    with col5:
        if st.session_state.title_recommender_result_page > 0:
            if st.button("⬅️ Previous Page"):
                st.session_state.title_recommender_result_page -= 1
                rerun()
        else:
            st.write("")

    with col6:
        st.markdown(f"<div style='text-align: center; font-size: 18px;'>{start+1} - {min(end, len(results))} of {len(results)}</div>", unsafe_allow_html=True)

    with col7:
        if end < len(results):
            if st.button("Next Page ➡️"):
                st.session_state.title_recommender_result_page += 1
                rerun()
        else:
            st.write("")

# ---- Sidebar Navigation ----
st.sidebar.title("🎬 Anime Recommender System")
page = st.sidebar.radio("Choose a module:", 
                        ["Main Page", "Item-Based Collaborative Filtering"])

animes, reviews = load_data()

if page == "Main Page":
    st.title("Welcome to Anime Recommender System")

elif page == "Item-Based Collaborative Filtering":
    st.title("Item-Based Collaborative Filtering Recommender")

    anime_selected = st.text_input("Select anime you like:", "Toradora!")

    if st.button("Get Recommendations"):
        with st.status("🔄 Processing... please wait", expanded=False):
            session_state_format()
            animes, reviews = load_data()

            anime_map = dict(zip(animes['uid'].astype(str), animes['title']))
            reviews['title'] = reviews['anime_uid'].astype(str).map(anime_map)
            reviews = reviews.dropna(subset=['title'])

            if reviews.empty:
                st.error("No valid review data found after title mapping.")
                st.stop()

            reviews['rating'] = pd.to_numeric(reviews['rating'], errors='coerce')

            anime_user_matrix = reviews.pivot_table(
                index='title', columns='profile', values='rating'
            ).fillna(0)

            if anime_user_matrix.empty:
                st.error("Not enough data to compute similarities.")
                st.stop()

            anime_similarity = cosine_similarity(anime_user_matrix)
            anime_similarity_df = pd.DataFrame(
                anime_similarity,
                index=anime_user_matrix.index,
                columns=anime_user_matrix.index
            )

            if anime_selected not in anime_similarity_df.index:
                st.warning("Anime title not found in data.")
                st.write(pd.DataFrame(columns=["title", "similarity", "genre", "score", "synopsis", "link"]))
                st.stop()

            sim_scores = anime_similarity_df[anime_selected].sort_values(ascending=False)
            sim_scores = sim_scores.drop(anime_selected)

            top = sim_scores.head(st.session_state.recommended_count + 1).reset_index()
            top.columns = ["title", "similarity"]

            available_cols = [c for c in ['title', 'genre', 'score', 'synopsis', 'link'] if c in animes.columns]
            anime_info = animes[available_cols].drop_duplicates(subset="title")

            result = top.merge(anime_info, on="title", how="left")

            result.rename(columns={
                'title': 'Title',
                'genre': 'Genre',
                'score': 'Rating',
                'link': 'Link',
                'similarity': 'Similarity'
            }, inplace=True)

            st.session_state.title_recommender_anime_select_details = animes[animes['title'] == anime_selected].rename(columns={
                'title': 'Title',
                'score': 'Rating',
                'link': 'Link',
                'genre': 'Genre'
            })

            st.session_state.title_recommender_results = result
            st.session_state.title_recommender_result_page = 0

        display_title_based_recommendations()
