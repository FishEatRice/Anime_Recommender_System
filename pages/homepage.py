import streamlit as st
from function.data_loader import load_data

from function.scraper import get_cover_image
from function.recommender import recommend

df = load_data()

st.title("🎯 Anime Recommender System")
st.write("选择你喜欢的动漫，系统会推荐相似的作品（按评分排序）")

anime_list = df['Title'].dropna().unique()
selected_anime = st.selectbox("选择动漫", anime_list)

if st.button("推荐"):
    results = recommend(
        df,
        selected_anime,
        top_n=st.session_state.get('recommended_count', 6),
        filter_hentai=st.session_state.get('filter_hentai', True)
    )

    if results.empty:
        st.warning("未找到相关动漫")
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