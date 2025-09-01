import streamlit as st
import pandas as pd

def session_state_format():

    if 'recommended_count' not in st.session_state:
        st.session_state.recommended_count = 9

    if 'filter_18' not in st.session_state:
        st.session_state.filter_18 = False
                
    if 'fast_search' not in st.session_state:
        st.session_state.fast_search = False

    if 'filter_rating' not in st.session_state:
        st.session_state.filter_rating = 0.0

    if "title_recommender_result_page" not in st.session_state:
        st.session_state.title_recommender_result_page = 0

    if "title_recommender_results" not in st.session_state:
        st.session_state.title_recommender_results = pd.DataFrame()

    if "title_recommender_anime_select_details" not in st.session_state:
        st.session_state.title_recommender_anime_select_details = pd.DataFrame()

    if "where_page" not in st.session_state:
        st.session_state.where_page = "main"

def session_state_reset_full():
    st.session_state.recommended_count = 9
    st.session_state.filter_18 = False
    st.session_state.fast_search = False
    st.session_state.filter_rating = 0.0
    st.session_state.title_recommender_result_page = 0
    st.session_state.title_recommender_results = pd.DataFrame()
    st.session_state.title_recommender_anime_select_details = pd.DataFrame()

def session_state_reset_anime_title():
    if st.session_state.where_page != "anime_title_recommender_page":
        st.session_state.title_recommender_result_page = 0
        st.session_state.title_recommender_results = pd.DataFrame()
        st.session_state.title_recommender_anime_select_details = pd.DataFrame()

def session_check_where():
    session_state_reset_anime_title()