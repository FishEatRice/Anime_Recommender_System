# Import UI
import streamlit as st

# Import Pandas
import pandas as pd

# CSV clearing
import ast

# Get Anime Picture
import requests

# Read and Clean Data From CSV
@st.cache_data
def load_data():
    df = pd.read_csv("../Anime_data.csv")

    # if Genre is null, then make all data to '' 
    
    # Why using ast.literal_eval(x):
        # Our Genre data is in ['Action', 'Adventure'] format 
        # After process becomes "Action Adventure" format
    
    df['Genre'] = df['Genre'].apply(lambda x: ' '.join(ast.literal_eval(x)) if pd.notnull(x) else '')

    return df

df = load_data()

# Get Anime Picture
@st.cache_data
def get_anime_picture(url):
    try:
        response = request.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        img_tag = soup.find("img", {"itemprop": "image"})

        if img_tag:
            # Catch src picture link
            return img_tag.get("data-src") or img_tag.get("src")

    except Exception:
        # If having error or not found
        return None

    return None
    
# Take related 
@st.cache_data(show_spinner = False)
def compute_same_genre(clean_df):
    # Ignore English Word, avoid extra text in keyin
    tfidf = TfidVectorizer(stop_words='english')
    
    # Put as matrix form
    tfidf_matrix = tfidf.fit_transform(filtered_df['Genre'])
    
    # Find Similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

# Recommend System
def recommend_system(anime_name, number=6, filter_hentai=True):
    # Check hentai or not?
    if filter_hentai:
        df_filtered = df[~df['Genre'].str.contains("Hentai", case=False, na=False)].reset_index(drop=True)

    else:
        df_filtered = df.reset_index(drop=True)

    if anime_name not in df_filtered['Title'].values:
        # If not inside filtered data

        if anime_name in df['Title'].values:
            st.warning(f"Warning: '{anime_name}' has been filtered, may have 'Hentai' label.")
        else:
            st.warning(f"'{anime_name}' not found.")

        return pd.DataFrame()

    # Call compute process
    cosine_sim_filtered = compute_same_genre(df_filtered)

    # Find anime from df_filtered
    idx = df_filtered[df_filtered['Title'] == anime_name].index[0]

    # Find similarly ranking
    sim_scores = list(enumerate(cosine_sim_filtered[idx]))
    # Sort similarly ranking
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Remove self (number 1)
    sim_scores = sim_scores[1:number + 1]
    anime_indices = [i[0] for i in sim_scores]

    # Return data that already put as 'High rating star' to 'low rating star'
    return df_filtered.iloc[anime_indices][['Title','Genre','Rating','Link','Synopsis']].sort_values(by='Rating', ascending=False)

# Streamlit Page Setup
st.set_page_config(page_title="Anime Recommender", layout="wide")

# Clear session_state
if 'display_anime_number' not in st.session_state:
    # Default 6 display
    st.session_state.display_anime_number = 6

if 'filter_hentai' not in st.session_state:
    # Default close
    st.session_state.filter_hentai = True

# Page Header
st.
        