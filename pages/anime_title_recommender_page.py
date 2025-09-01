import streamlit as st
from data.data_loader import load_data
from data.data_catch import get_anime_picture
import pandas as pd
from data.data_session import session_state_format
from streamlit.commands.execution_control import rerun
from streamlit_scroll_to_top import scroll_to_here
from function.anime_related_recommender import recommend
from data.data_session import session_check_where

# Format session_state
session_state_format()

# Check Where
st.session_state.where_page = "anime_title_recommender_page"
session_check_where()

df = load_data()

def anime_in_18(row, filter_status):
    title = row['Title']
    if not filter_status and row['18+']:
        return f"[🔞18+] {title}"
    else:
        return title

# To Top every time refresh
scroll_to_here(0, key="top")

st.title("Anime Recommender System")
st.write("Please choose the anime that you like, system will recommended a related anime.")

anime_list = df['Title'].dropna().unique()

# Display Mother Fucker State
# Everytime stuck stuck stuck
st.write("Current session state:", {
    "recommended_count": st.session_state.recommended_count,
    "filter_18": st.session_state.filter_18,
    "filter_rating": st.session_state.filter_rating,
    "fast_search": st.session_state.fast_search,
    "title_recommender_result_page": st.session_state.title_recommender_result_page,
    "Where Am I": st.session_state.where_page
})

# Filter 18+
if st.session_state.filter_18:
    anime_list = df[~df['18+']]['Title'].unique()
else:
    anime_list = [anime_in_18(row, st.session_state.filter_18) for _, row in df.iterrows()]

col1, col2 = st.columns([4, 1])
with col1:
    selected_anime = st.selectbox("Choose One Anime", anime_list)

with col2:
    st.markdown("<div style='padding-top: 28px'></div>", unsafe_allow_html=True)
    recommend_clicked = st.button("Recommend")

if recommend_clicked:

    st.session_state.title_recommender_result_page = 0
    st.session_state.anime_title_result = 1
    st.session_state.title_recommender_results = pd.DataFrame()
    st.session_state.title_recommender_anime_select_details = pd.DataFrame()

    st.markdown("---")
    selected_anime = selected_anime.replace("[🔞18+] ", "") 

    title_recommender_results, title_recommender_anime_select_details = recommend(
        df,
        selected_anime,
        filter_18   = st.session_state.get('filter_18', True),
        filter_rating   = st.session_state.get('filter_rating', 0.0)
    )

    st.session_state.title_recommender_results = title_recommender_results
    st.session_state.title_recommender_anime_select_details = title_recommender_anime_select_details
    # ---

if not st.session_state.title_recommender_results.empty and not st.session_state.title_recommender_anime_select_details.empty:
# ---
    st.write("Anime Selected:")

    # Anime Selected Details
    title_recommender_anime_select_details = st.session_state.title_recommender_anime_select_details
    title = title_recommender_anime_select_details.iloc[0]['Title']
    link = title_recommender_anime_select_details.iloc[0]['Link']
    rating = title_recommender_anime_select_details.iloc[0]['Rating']
    genre = title_recommender_anime_select_details.iloc[0]['Genre']
    votes = title_recommender_anime_select_details.iloc[0]['Votes']

    votes_display = 0 if pd.isna(votes) else int(votes)
    rating = 0.0 if pd.isna(rating) else rating

    if st.session_state.fast_search != True:
        col3, col4 = st.columns([1,3])
        
        with col3:
            img_url = get_anime_picture(title_recommender_anime_select_details.iloc[0]['Link'])
            if img_url:
                st.image(img_url, width=150)

        with col4:
            st.write("")
            st.write("")
            st.write("")
            st.markdown(f"[{title}]({link})")
            st.write(f"⭐ {rating:.2f} / 10.0 ( {votes_display} 👥)")
            st.caption(genre)
    else:
        st.markdown(f"[{title}]({link})")
        st.write(f"⭐ {rating:.2f} / 10.0 ( {votes_display} 👥)")
        st.caption(genre)

    st.markdown("---")

    per_page = st.session_state.get('recommended_count', 9)
    start = st.session_state.title_recommender_result_page * per_page
    end = start + per_page
    
    title_recommender_results = st.session_state.title_recommender_results
    
    page_results = title_recommender_results.iloc[start:end]

    st.write(f"Recommend Anime:")

    # Show only current page
    for row_start in range(0, len(page_results), 3):
        cols = st.columns(3, gap="medium")
        for col, (_, row) in zip(cols, page_results.iloc[row_start:row_start+3].iterrows()):
            with col:
                if st.session_state.fast_search != True:
                    img_url = get_anime_picture(row['Link'])
                    if img_url:
                        st.image(img_url, width=150)
                st.markdown(f"[{row['Title']}]({row['Link']})")
                st.write(f"⭐ {row['Rating']} / 10.0 ( {int(row['Votes'])} 👥)")
                st.caption(row['Genre'])
        st.markdown("---")

    # Navigation buttons
    col5, col6, col7 = st.columns([1,2,1])
    with col5:
        if st.session_state.title_recommender_result_page > 0:
            if st.button("⬅️ Previous Page"):
                st.session_state.title_recommender_result_page -= 1
                rerun()
        else:
            st.write("")
    
    with col6:
        st.markdown(f"<div style='text-align: center; font-size: 18px; padding-top: 10px'>{start+1} - {min(end, len(title_recommender_results))} of {len(title_recommender_results)}</div>", unsafe_allow_html=True)

    with col7:
        if end < len(title_recommender_results):
            if st.button("Next Page ➡️"):
                st.session_state.title_recommender_result_page += 1
                rerun()
        else:
            st.write("")
