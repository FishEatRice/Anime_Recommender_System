import streamlit as st
from function.data_loader import load_data
from function.scraper import get_cover_image
from function.recommender import recommend_by_keyword

# 加载数据
df = load_data()

st.title("🔍 基于关键词的动漫推荐")
st.write("输入你喜欢的类型或主题，我们将推荐相关动漫")

keyword = st.text_input("输入关键词", "Action")

if st.button("推荐"):
    results = recommend_by_keyword(
        df,
        keyword,
        top_n=st.session_state.get('recommended_count', 6),
        filter_hentai=st.session_state.get('filter_hentai', True)
    )

    if results.empty:
        st.warning("没有找到相关的动漫")
    else:
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
