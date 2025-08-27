import streamlit as st
from streamlit.commands.execution_control import rerun
from data.data_session import session_state_reset

# Format session_state
session_state_reset()
    
st.write("Current session state:", {
    "recommended_count": st.session_state.recommended_count,
    "filter_hentai": st.session_state.filter_hentai,
    "filter_rating": st.session_state.filter_rating,
    "fast_search": st.session_state.fast_search,
})

st.title("Settings")

# Reset all filters button
if st.button("🔄 Reset All Filters"):
    st.session_state.recommended_count = 9
    st.session_state.filter_hentai = True
    st.session_state.filter_rating = 0.00
    st.session_state.fast_search = False
    rerun()
    
# Hentai Filter
st.markdown("<br>", unsafe_allow_html=True)
filter_hentai = st.checkbox(
    "'Hentai' related Anime Filter",
    value=st.session_state.get('filter_hentai', True)
)
if st.session_state.filter_hentai != filter_hentai:
    st.session_state.filter_hentai = filter_hentai
    rerun()

# Fast Search
st.markdown("<br>", unsafe_allow_html=True)
fast_search = st.checkbox(
    "Fast Search - Skip catch image during process",
    value=st.session_state.get('fast_search', False)
)
if st.session_state.fast_search != fast_search:
    st.session_state.fast_search = fast_search
    rerun()

# Result Count
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns([8, 1])
with col1:
    recommended_count = st.slider(
        "Result Count",
        min_value=3,
        max_value=21,
        step=3,
        value=st.session_state.recommended_count,
    )

with col2:
    if st.button("Reset", key="reset_result_count"):
        recommended_count = 9
        
if st.session_state.recommended_count != recommended_count:
    st.session_state.recommended_count = recommended_count
    rerun()

# Rating Filter
st.markdown("<br>", unsafe_allow_html=True)
col3, col4 = st.columns([8, 1])
with col3:
    filter_rating = st.slider(
        "Rating Filter (0 - Show All) (10 - Will be harder to find anime)",
        min_value=0.0,
        max_value=10.0,
        step=0.01,
        value=st.session_state.filter_rating, 
    )

with col4:
    if st.button("Reset", key="reset_filter_rating"):
        filter_rating = 0.0

if st.session_state.filter_rating != filter_rating:
    st.session_state.filter_rating = filter_rating
    rerun()