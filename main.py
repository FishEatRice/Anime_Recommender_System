import streamlit as st
from data.data_loader import load_data
from data.data_catch import get_anime_picture
from function.anime_related_recommender import recommend
from data.data_session import session_state_reset

# Format session_state
session_state_reset()

df = load_data()

def anime_in_18(row, filter_status):
    title = row['Title']
    if not filter_status and row['18+']:
        return f"[🔞18+] {title}"
    else:
        return title

st.title("Anime Recommender System")
st.write("Please choose the anime that you like, system will recommended a related anime.")

anime_list = df['Title'].dropna().unique()

st.write("Current session state:", {
    "recommended_count": st.session_state.recommended_count,
    "filter_18": st.session_state.filter_18,
    "filter_rating": st.session_state.filter_rating,
    "fast_search": st.session_state.fast_search,
})

# Filter 18+
if st.session_state.filter_18:
    anime_list = df[~df['18+']]['Title'].unique()
else:
    anime_list = [anime_in_18(row, st.session_state.filter_18) for _, row in df.iterrows()]

selected_anime = st.selectbox("Choose One Anime", anime_list)

if st.button("Recommend"):

    selected_anime = selected_anime.replace("[🔞18+] ", "") 

    results = recommend(
        df,
        selected_anime,
        result_count    = st.session_state.get('recommended_count', 9),
        filter_18   = st.session_state.get('filter_18', True),
        filter_rating   = st.session_state.get('filter_rating', 0.0)
    )

    if results.empty:
        st.warning("Cannot found any related anime")
        if st.session_state.filter_rating > 0.0:
            st.error("Try to low the rating filter")
            
    else:
        for row_start in range(0, len(results), 3):
            cols = st.columns(3, gap="medium")
            for col, (_, row) in zip(cols, results.iloc[row_start:row_start + 3].iterrows()):
                with col:
                    if st.session_state.fast_search != True:
                        img_url = get_anime_picture(row['Link'])
                        if img_url:
                            st.image(img_url, width=150)
                    
                    st.markdown(f"[{row['Title']}]({row['Link']})")
                    st.write(f"⭐ {row['Rating']} / 10.0")
                    st.caption(row['Genre'])