import streamlit as st
from session.data_session import *
from data.data_loader import load_data
from streamlit_scroll_to_top import scroll_to_here

st.title("Settings Page")

session_state_format()
st.session_state.where_page = "settings_page"
session_check_where()

df_animes, df_reviews = load_data()

scroll_to_here(0, key="top")