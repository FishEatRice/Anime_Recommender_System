import streamlit as st
from session.data_session import *
from data.data_loader import load_data
from streamlit_scroll_to_top import scroll_to_here

st.title("Settings Page")

session_state_format()
st.session_state.where_page = "settings_page"
session_check_where()

scroll_to_here(0, key="top")

def update_session_states(key, value):
    st.session_state[key] = value
    st.rerun()

# --- Fast Search ---
st.markdown("<br>", unsafe_allow_html=True)
fast_search = st.checkbox(
    "Fast Search - Skip catch image during process",
    value=st.session_state.get("fast_search", False),
)

if fast_search != st.session_state.get("fast_search", False):
    update_session_states("fast_search", fast_search)

# --- Result Count ---
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns([8, 1])

with col1:
    recommended_count = st.slider(
        "Result Count",
        min_value=3,
        max_value=21,
        step=3,
        value=st.session_state.get("recommended_count", 9),
    )

with col2:
    if st.button("Reset", key="reset_result_count"):
        recommended_count = 9
        update_session_states("recommended_count", recommended_count)

if recommended_count != st.session_state.get("recommended_count", 9):
    update_session_states("recommended_count", recommended_count)
