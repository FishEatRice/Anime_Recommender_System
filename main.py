import streamlit as st
from function.data_loader import load_data

# 初始化 session_state
if 'recommended_count' not in st.session_state:
    st.session_state.recommended_count = 6
if 'filter_hentai' not in st.session_state:
    st.session_state.filter_hentai = True

# 加载数据
df = load_data()

st.Page("homepage.py", title="test 1"),