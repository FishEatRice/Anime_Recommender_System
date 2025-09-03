import streamlit as st

pages = {
    "🏠Main": [st.Page("pages/main_page.py", title="Main Page")],
    "🕵️Recommender System": [
        st.Page("pages/anime_title_recommender_page.py", title="Anime Title"),
        st.Page("pages/anime_genre_recommender_page.py", title="Anime Genre"),
    ],
    "⚙️Settings": [st.Page("pages/settings_page.py", title="Settings Page")],
}

pg = st.navigation(pages)
pg.run()


st.Page("pages/main_page.py", title="Main Page")