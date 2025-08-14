import streamlit as st
import pandas as pd
import ast
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. 数据加载
@st.cache_data
def load_data():
    df = pd.read_csv("../Anime_data.csv")
    df['Genre'] = df['Genre'].apply(lambda x: ' '.join(ast.literal_eval(x)) if pd.notnull(x) else '')
    return df

df = load_data()

# 2. 抓取封面图
@st.cache_data
def get_cover_image(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        img_tag = soup.find("img", {"itemprop": "image"})
        if img_tag:
            return img_tag.get("data-src") or img_tag.get("src")
    except Exception:
        return None
    return None

# 3. 相似度计算
@st.cache_data
def compute_similarity():
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['Genre'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

cosine_sim = compute_similarity()

# 4. 推荐函数（按评分排序）
def recommend(anime_title, top_n=6):
    if anime_title not in df['Title'].values:
        return pd.DataFrame()
    idx = df.index[df['Title'] == anime_title][0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]
    anime_indices = [i[0] for i in sim_scores]
    return df.iloc[anime_indices][['Title', 'Genre', 'Rating', 'Link']].sort_values(by='Rating', ascending=False)

# 5. Streamlit UI
st.set_page_config(page_title="Anime Recommender", layout="wide")
st.title("🎯 Anime Recommender System")
st.write("选择你喜欢的动漫，系统会推荐相似的作品")

anime_list = df['Title'].dropna().unique()
selected_anime = st.selectbox("选择动漫", anime_list)

if st.button("推荐"):
    results = recommend(selected_anime, top_n=6)
    if results.empty:
        st.warning("没找到相关动漫")
    else:
        for row_start in range(0, len(results), 3):
            cols = st.columns(3, gap="large")  # 三列且间距大
            for col, (_, row) in zip(cols, results.iloc[row_start:row_start+3].iterrows()):
                with col:
                    img_url = get_cover_image(row['Link'])
                    if img_url:
                        st.image(img_url, width=150)
                    st.markdown(f"**[{row['Title']}]({row['Link']})**")
                    st.write(f"⭐ {row['Rating']}")
                    st.caption(row['Genre'])
            st.markdown("<br><br>", unsafe_allow_html=True)  # 每行底部留空白
