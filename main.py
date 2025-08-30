import streamlit as st
from data.data_session import session_state_reset

# Format session_state
session_state_reset()

pages = [
    st.Page("pages/anime_title_recommender_page.py", title="Anime Title Recommender"),
    st.Page("pages/settings_page.py", title="Settings")
]

pg = st.navigation(pages, position="top")
pg.run()

st.Page("pages/anime_title_recommender_page.py", title="Anime Recommender")