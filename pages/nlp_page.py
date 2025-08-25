import streamlit as st
import pandas as pd
from function.scraper import get_cover_image
from function.recommender import recommend, recommend_by_keyword
from function.query_parser import parse_user_query

def show(df):
    st.title("🗣 自然语言动漫推荐")
    st.write("你可以用语言输入，比如 Toradora 或者 I want anime with ghost")

    user_query = st.text_input("输入一句话", "Can I have something like Toradora")

    if st.button("搜索"):
        mode, value = parse_user_query(user_query, df)

        if mode == "title":
            st.info(f"检测到你想找和 *{value}* 类似的动漫")
            results = recommend(
                df,
                value,
                top_n=st.session_state.get('recommended_count', 6),
                filter_hentai=st.session_state.get('filter_hentai', True)
            )
        elif mode == "keyword":
            st.info(f"检测到你想找包含 *{value}* 类型的动漫")
            results = recommend_by_keyword(
                df,
                value,
                top_n=st.session_state.get('recommended_count', 6),
                filter_hentai=st.session_state.get('filter_hentai', True)
            )
        else:
            st.warning("无法理解你的请求，请尝试换个说法")
            results = pd.DataFrame()

        if not results.empty:
            for row_start in range(0, len(results), 3):
                cols = st.columns(3, gap="large")
                for col, (_, row) in zip(cols, results.iloc[row_start:row_start + 3].iterrows()):
                    with col:
                        img_url = get_cover_image(row['Link'])
                        if img_url:
                            st.image(img_url, width=150)
                        st.markdown(f"[{row['Title']}]({row['Link']})")
                        st.write(f"⭐ {row['Rating']}")
                        st.caption(row['Genre'])
