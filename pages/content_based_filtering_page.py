import streamlit as st
from session.data_session import *
from data.data_loader import *
from streamlit_scroll_to_top import scroll_to_here
import pandas as pd
from function.content_based_filtering_function import content_based_filtering_recommend

st.title("Content-Based")

session_state_format()
st.session_state.where_page = "content_based_page"
session_check_where()

df_animes, df_reviews = load_data()

scroll_to_here(0, key="top")

def prev_page():
    st.session_state.content_based_result_page -= 1

def next_page():
    st.session_state.content_based_result_page += 1

col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_input(
        "NLP System",
        label_visibility="visible",
        disabled=False,
        placeholder="Is there any sports high school anime recommended?",
        value="Is there any sports high school anime recommended?"
    )

with col2:
    st.markdown("<div style='padding-top: 28px'></div>", unsafe_allow_html=True)
    recommend_clicked = st.button("Recommend", key="recommend_btn")

if recommend_clicked:

    if not user_input:
        user_input = "Is there any sports high school anime recommended?"
     
    st.session_state.content_based_result_page = 0
    st.session_state.content_based_results = pd.DataFrame()
    st.session_state.user_input = pd.DataFrame()

    st.markdown("---")
    st.session_state.content_based_results, st.session_state.user_input = content_based_filtering_recommend(
        df_animes,
        user_input
    )

    st.info(f"Your Finding: {st.session_state.user_input}")

    page_results = content_based_filtering_recommend(df_animes, user_input)

if (
    st.session_state.content_based_results.empty
    or not st.session_state.user_input
):
    st.error("Please click recommend button one more time or No related anime found.")

else:
    
    if st.session_state.user_input == user_input:

        per_page = st.session_state.get('recommended_count', 9)
        current_result_page = st.session_state.content_based_result_page
        start = current_result_page * per_page
        end = start + per_page
        
        content_recommender_results = st.session_state.content_based_results
        
        page_results = content_recommender_results.iloc[start:end]

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
                    genre_text = str(row['genre']).strip("[]").replace("'", "").strip().replace(", ", " | ")
                    st.caption(genre_text)
            st.markdown("---")

        col5, col6, col7 = st.columns([1, 2, 1])
        with col5:
            if st.session_state.content_based_result_page > 0:
                st.button("⬅️ Previous Page", on_click=prev_page, key="prev_btn")
            else:
                st.write("")

        with col6:
            st.markdown(f"<div style='text-align: center; font-size: 18px;'>{start+1} - {min(end, len(content_recommender_results))} of {len(content_recommender_results)}</div>", unsafe_allow_html=True)

        with col7:
            if end < len(content_recommender_results):
                st.button("Next Page ➡️", on_click=next_page, key="next_btn")

            else:
                st.write("")



