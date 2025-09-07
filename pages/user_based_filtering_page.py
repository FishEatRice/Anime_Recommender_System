import streamlit as st
from session.data_session import *
from data.data_loader import *
from streamlit_scroll_to_top import scroll_to_here
import pandas as pd
from function.user_based_filtering_function import user_based_filtering_recommend

st.title("User-Based Collaborative Filtering")

session_state_format()
st.session_state.where_page = "user_based_page"
session_check_where()

df_animes, df_reviews = load_data()

scroll_to_here(0, key="top")

anime_list = df_animes['title'].dropna().unique()

def prev_page():
    st.session_state.user_based_result_page -= 1

def next_page():
    st.session_state.user_based_result_page += 1

col1, col2 = st.columns([4, 1])
with col1:
    selected_anime = st.selectbox("Choose One Anime", anime_list)

with col2:
    st.markdown("<div style='padding-top: 28px'></div>", unsafe_allow_html=True)
    recommend_clicked = st.button("Recommend", key="recommend_btn")

if recommend_clicked:

    st.session_state.user_based_result_page = 0
    st.session_state.user_based_results = pd.DataFrame()
    st.session_state.user_based_anime_select_details = pd.DataFrame()

    st.markdown("---")
    st.session_state.user_based_results, st.session_state.user_based_anime_select_details = user_based_filtering_recommend(
        df_animes,
        df_reviews,
        selected_anime
    )

if (
    st.session_state.user_based_results.empty
    or st.session_state.user_based_anime_select_details.empty
):
    st.error("Please click recommend button one more time or Anime details not found.")

else:
    details = st.session_state.user_based_anime_select_details.iloc[0]
    
    if details['title'] == selected_anime:

        user_based_anime_select_details = st.session_state.user_based_anime_select_details
        
        title = user_based_anime_select_details.iloc[0]['title']
        genre = user_based_anime_select_details.iloc[0]['genre']
        rating = user_based_anime_select_details.iloc[0]['score']
        synopsis = user_based_anime_select_details.iloc[0]['synopsis']
        link = user_based_anime_select_details.iloc[0]['link']

        if st.session_state.fast_search != True:
            col3, col4 = st.columns([1,3])
            
            with col3:
                img_url = get_anime_picture(link)
                if img_url:
                    st.image(img_url, width=150)

            with col4:
                st.write("")
                st.write("")
                st.write("")
                st.markdown(f"[{title}]({link})")
                st.write(f"⭐ {rating:.2f} / 10.0")
                genre_text = str(genre).strip("[]").replace("'", "").strip().replace(", ", " | ")
                st.caption(genre_text)

        else:
            st.markdown(f"[{title}]({link})")
            st.write(f"⭐ {rating:.2f} / 10.0")
            genre_text = str(genre).strip("[]").replace("'", "").strip().replace(", ", " | ")
            st.caption(genre_text)
            
        st.markdown("---")

        per_page = st.session_state.get('recommended_count', 9)
        current_result_page = st.session_state.user_based_result_page
        start = current_result_page * per_page
        end = start + per_page
        
        title_recommender_results = st.session_state.user_based_results
        
        page_results = title_recommender_results.iloc[start:end]

        st.write(f"Recommend Anime:")

        # Show only current page
        for row_start in range(0, len(page_results), 3):
            cols = st.columns(3, gap="medium")
            for col, (_, row) in zip(cols, page_results.iloc[row_start:row_start+3].iterrows()):
                with col:
                    if st.session_state.fast_search != True:
                        img_url = get_anime_picture(row['link'])
                        if img_url:
                            st.image(img_url, width=150)
                    st.markdown(f"[{row['title']}]({row['link']})")
                    st.write(f"⭐ {row['score']:.2f} / 10.0")
                    st.write(f"Predicted Score: {row['predicted_score']:.2f}")
                    genre_text = str(row['genre']).strip("[]").replace("'", "").strip().replace(", ", " | ")
                    st.caption(genre_text)
            st.markdown("---")

        col5, col6, col7 = st.columns([1, 2, 1])
        with col5:
            if st.session_state.user_based_result_page > 0:
                st.button("⬅️ Previous Page", on_click=prev_page, key="prev_btn")
            else:
                st.write("")

        with col6:
            st.markdown(f"<div style='text-align: center; font-size: 18px;'>{start+1} - {min(end, len(title_recommender_results))} of {len(title_recommender_results)}</div>", unsafe_allow_html=True)

        with col7:
            if end < len(title_recommender_results):
                st.button("Next Page ➡️", on_click=next_page, key="next_btn")

            else:
                st.write("")
