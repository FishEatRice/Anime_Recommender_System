import streamlit as st
from data.data_loader import load_data
from data.data_catch import get_anime_picture
from function.anime_related_recommender import recommend
from data.data_session import session_state_reset

# Format session_state
session_state_reset()

df = load_data()

st.title("Anime Recommender System")
st.write("Please choose the anime that you like, system will recommended a related anime.")

anime_list = df['Title'].dropna().unique()

# Filter hentai
if st.session_state.filter_hentai:
    anime_list = df[~df['Genre'].str.contains("Hentai", case=False, na=False)]['Title'].unique()

selected_anime = st.selectbox("Choose One Anime", anime_list)

if st.button("Recommend"):
    results = recommend(
        df,
        selected_anime,
        result_count    = st.session_state.get('recommended_count', 9),
        filter_hentai   = st.session_state.get('filter_hentai', True),
        filter_rating   = st.session_state.get('filter_rating', 7.50)
    )

    if results.empty:
        st.warning("Cannot found any related anime")

    else:
        for row_start in range(0, len(results), 3):
            cols = st.columns(3, gap="medium")
            for col, (_, row) in zip(cols, results.iloc[row_start:row_start + 3].iterrows()):
                with col:
                    img_url = get_anime_picture(row['Link'])
                    if img_url:
                        st.image(img_url, width=150)
                    
                    st.markdown(f"[{row['Title']}]({row['Link']})")
                    st.write(f"⭐ {row['Rating']} / 10.0")
                    st.caption(row['Genre'])