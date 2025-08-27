import streamlit as st

def session_state_reset():

    if 'recommended_count' not in st.session_state:
        st.session_state.recommended_count = 9

    if 'filter_hentai' not in st.session_state:
        st.session_state.filter_hentai = True
                
    if 'fast_search' not in st.session_state:
        st.session_state.fast_search = False

    if 'filter_rating' not in st.session_state:
        st.session_state.filter_rating = 0.0