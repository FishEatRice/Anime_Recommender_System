import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. 数据加载
@st.cache_data
def load_data():
    df = pd.read_csv("../Anime_data.csv")
    df = df.dropna(subset=['Genre'])  # 去掉没有类型的动漫
    return df

df = load_data()

# 2. 特征提取（TF-IDF）
@st.cache_data
def compute_similarity():
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['Genre'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

cosine_sim = compute_similarity()

# 3. 推荐函数
def recommend(anime_title, top_n=5):
    if anime_title not in df['Title'].values:
        return []
    idx = df.index[df['Title'] == anime_title][0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]  # 排除自己
    anime_indices = [i[0] for i in sim_scores]
    return df.iloc[anime_indices][['Title', 'Genre']]

# 4. Streamlit UI
st.title("🎯 Anime Recommender System")
st.write("输入你喜欢的动漫，系统会推荐相似的作品")

anime_list = df['Title'].dropna().unique()
selected_anime = st.selectbox("选择动漫", anime_list)

if st.button("推荐"):
    results = recommend(selected_anime, top_n=5)
    if results.empty:
        st.warning("没找到相关动漫")
    else:
        for i, row in results.iterrows():
            st.write(f"**{row['Title']}** - {row['Genre']}")
