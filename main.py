import streamlit as st
from data.data_loader import load_data
from data.data_catch import get_anime_picture

# Format session_state
if 'recommended_count' not in st.session_state:
    st.session_state.recommended_count = 9
if 'filter_hentai' not in st.session_state:
    st.session_state.filter_hentai = True

df = load_data()

st.title("Anime Recommender System")
st.write("Please choose the anime that you like, system will recommended a related anime.")

anime_list = df['Title'].dropna().unique()
selected_anime = st.selectbox("Choose One Anime", anime_list)


