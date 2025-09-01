import streamlit as st

pages = [
    st.Page("pages/anime_title_recommender_page.py", title="Anime Title Recommender"),
    st.Page("pages/anime_genre_recommender_page.py", title="Anime Genre Recommender"),
    st.Page("pages/settings_page.py", title="Settings")
]

pg = st.navigation(pages, position="top")
pg.run()

st.Page("pages/anime_title_recommender_page.py", title="Anime Recommender")