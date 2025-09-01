import streamlit as st
from data.data_loader import load_data
from data.data_catch import get_anime_picture
import pandas as pd
from data.data_session import session_state_format
from streamlit.commands.execution_control import rerun
from streamlit_scroll_to_top import scroll_to_here
from data.data_session import session_check_where

# Format session_state
session_state_format()

df = load_data()

# Check Where
st.session_state.where_page = "anime_genre_recommender_page"
session_check_where()

# Display Mother Fucker State
# Everytime stuck stuck stuck
st.write("Current session state:", {
    "recommended_count": st.session_state.recommended_count,
    "filter_18": st.session_state.filter_18,
    "filter_rating": st.session_state.filter_rating,
    "fast_search": st.session_state.fast_search,
    "title_recommender_result_page": st.session_state.title_recommender_result_page,
    "Where Am I": st.session_state.where_page
})