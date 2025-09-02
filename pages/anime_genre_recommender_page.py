import streamlit as st
from data.data_loader import load_data
from data.data_catch import get_anime_picture
import pandas as pd
from data.data_session import session_state_format
from streamlit.commands.execution_control import rerun
from streamlit_scroll_to_top import scroll_to_here
from data.data_session import session_check_where
from function.anime_genre_related_recommender import recommend

# Format session_state
session_state_format()

df = load_data()

# Check Where
st.session_state.where_page = "anime_genre_recommender_page"
session_check_where()

# Display Mother Fucker State
# Everytime stuck stuck stuck
st.write("Current session state:", {
    "recommended_count": st.session_state.recommended_count,
    "filter_18": st.session_state.filter_18,
    "filter_rating": st.session_state.filter_rating,
    "fast_search": st.session_state.fast_search,
    "genre_recommender_result_page": st.session_state.genre_recommender_result_page,
    "Where Am I": st.session_state.where_page
})

# To Top every time refresh
scroll_to_here(0, key="top")

st.title("Anime Recommender System")
st.write("Please choose the genres that you want, system will recommend related anime.")

# Initialize run flag
run_genre_recommender = 0  

# Build genre list
genre_list = (
    df['Genre']
    .dropna()
    .apply(lambda x: [g.strip() for g in x.split()])
    .explode()
    .unique()
)
genre_list = [g for g in genre_list if isinstance(g, str)]
genre_list = sorted(genre_list)

# Let user pick how many genres
num_genres = st.number_input(
    "How many genres do you want to choose?",
    min_value=1,
    max_value=5,
    value=1, 
    step=1
)

selected_genres = []
for i in range(num_genres):
    genre = st.selectbox(
        f"Choose Genre {i+1}",
        [g for g in genre_list if g not in selected_genres],
        key=f"genre_{i}"
    )
    selected_genres.append(genre)

# Recommend button
if st.button("Recommend"):
    # Update query params in the URL
    st.query_params["genre"] = selected_genres  

query_params = st.query_params
url_genre = []
if "genre" in query_params:
    url_genre = query_params.get_all("genre")

    if all(g in genre_list for g in url_genre) and len(url_genre) > 0:
        # Find Genre in list
        run_genre_recommender = 1
    else:
        # Having ?genre but no value
        run_genre_recommender = 2

elif len(query_params) == 0:
    # No Genre in URL
    run_genre_recommender = 0

else:
    # No find in list
    run_genre_recommender = 2

if url_genre:
    selected_genres = url_genre

if run_genre_recommender == 1:
    st.session_state.genre_recommender_result_page = 0
    st.session_state.genre_recommender_results = recommend(
        df,
        selected_genres,
        filter_18=st.session_state.get('filter_18', True),
        filter_rating=st.session_state.get('filter_rating', 0.0)
    )

    results = st.session_state.genre_recommender_results

    per_page = st.session_state.get('recommended_count', 9)
    start = st.session_state.genre_recommender_result_page * per_page
    end = start + per_page
    page_results = results.iloc[start:end]

    # Refresh All
    run_genre_recommender = 0


    st.markdown("---")
    st.write(f"Recommended Anime:")

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

    # Pagination
    col5, col6, col7 = st.columns([1, 2, 1])
    with col5:
        if st.session_state.genre_recommender_result_page > 0:
            if st.button("⬅️ Previous Page"):
                st.session_state.genre_recommender_result_page -= 1
                rerun()
    with col6:
        st.markdown(
            f"<div style='text-align: center; font-size: 18px; padding-top: 10px'>"
            f"{start+1} - {min(end, len(results))} of {len(results)}</div>",
            unsafe_allow_html=True
        )
    with col7:
        if end < len(results):
            if st.button("Next Page ➡️"):
                st.session_state.genre_recommender_result_page += 1
                rerun()

elif run_genre_recommender > 1 :
    st.warning("Genre not found, please try again.")