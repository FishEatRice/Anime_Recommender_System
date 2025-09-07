import streamlit as st
import pandas as pd

def session_state_format():

    if 'recommended_count' not in st.session_state:
        st.session_state.recommended_count = 9
                
    if 'fast_search' not in st.session_state:
        st.session_state.fast_search = False

    # Item Based Recommender Result Page
    if "item_based_result_page" not in st.session_state:
        st.session_state.item_based_result_page = 0

    if "item_based_results" not in st.session_state:
        st.session_state.item_based_results = pd.DataFrame()

    if "item_based_anime_select_details" not in st.session_state:
        st.session_state.item_based_anime_select_details = pd.DataFrame()

    # User Based Recommender Result Page
    if "user_based_result_page" not in st.session_state:
        st.session_state.user_based_result_page = 0

    if "user_based_results" not in st.session_state:
        st.session_state.user_based_results = pd.DataFrame()

    if "user_based_anime_select_details" not in st.session_state:
        st.session_state.user_based_anime_select_details = pd.DataFrame()

    # Where am I
    if "where_page" not in st.session_state:
        st.session_state.where_page = "Null"

def session_check_where():
    if st.session_state.where_page != "item_based_page":
        st.session_state.item_based_result_page = 0
        st.session_state.item_based_results = pd.DataFrame()
        st.session_state.item_based_anime_select_details = pd.DataFrame()
    if st.session_state.where_page != "user_based_page":
        st.session_state.user_based_result_page = 0
        st.session_state.user_based_results = pd.DataFrame()
        st.session_state.user_based_anime_select_details = pd.DataFrame()