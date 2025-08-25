import streamlit as st

st.title("⚙ 设置")
st.write("自定义推荐数量和是否过滤 Hentai 类型")

recommended_count = st.slider("每次推荐数量", min_value=3, max_value=21, value=st.session_state.get('recommended_count', 6), step=3)
st.session_state.recommended_count = recommended_count

filter_hentai = st.checkbox("过滤 Hentai 类型动漫", value=st.session_state.get('filter_hentai', True))
st.session_state.filter_hentai = filter_hentai
