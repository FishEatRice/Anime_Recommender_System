import streamlit as st
import pandas as pd

def session_state_reset():

    if 'recommended_count' not in st.session_state:
        st.session_state.recommended_count = 9

    if 'filter_18' not in st.session_state:
        st.session_state.filter_18 = False
                
    if 'fast_search' not in st.session_state:
        st.session_state.fast_search = False

    if 'filter_rating' not in st.session_state:
        st.session_state.filter_rating = 0.0

    if "result_page" not in st.session_state:
        st.session_state.result_page = 0

    if "results" not in st.session_state:
        st.session_state.results = pd.DataFrame()

    if "anime_select_details" not in st.session_state:
        st.session_state.anime_select_details = pd.DataFrame()