import streamlit as st
import pandas as pd
import ast
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# AI Detect
from fuzzywuzzy import process
import re

# 1. 数据加载
@st.cache_data
def load_data():
    df = pd.read_csv("../Anime_data.csv")
    df['Genre'] = df['Genre'].apply(lambda x: ' '.join(ast.literal_eval(x)) if pd.notnull(x) else '')
    return df

df = load_data()

# 2. 获取动漫封面图
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

# 3. 相似度计算函数（传入过滤后的 df）
@st.cache_data(show_spinner=False)
def compute_similarity(filtered_df):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(filtered_df['Genre'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

# 4. 推荐函数（按评分排序 + 正确过滤）
def recommend(anime_title, top_n=6, filter_hentai=True):
    if filter_hentai:
        df_filtered = df[~df['Genre'].str.contains("Hentai", case=False, na=False)].reset_index(drop=True)
    else:
        df_filtered = df.reset_index(drop=True)

    if anime_title not in df_filtered['Title'].values:
        st.warning(f"未找到名为 '{anime_title}' 的动漫，可能是因为该类型被过滤掉了。")
        if anime_title in df['Title'].values:
            st.warning("注意：该动漫原本存在，但它包含了 'Hentai' 类型，因此被过滤掉。")
        return pd.DataFrame()

    cosine_sim_filtered = compute_similarity(df_filtered)
    idx = df_filtered[df_filtered['Title'] == anime_title].index[0]
    sim_scores = list(enumerate(cosine_sim_filtered[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n + 1]
    anime_indices = [i[0] for i in sim_scores]
    return df_filtered.iloc[anime_indices][['Title', 'Genre', 'Rating', 'Link']].sort_values(by='Rating', ascending=False)

# 5. 关键词推荐函数（不使用相似度）
def recommend_by_keyword(keyword, top_n=6, filter_hentai=True):
    if filter_hentai:
        filtered_df = df[~df['Genre'].str.contains("Hentai", case=False, na=False)]
    else:
        filtered_df = df
    
    filtered_df = filtered_df[filtered_df['Genre'].str.contains(keyword, case=False, na=False)]
    return filtered_df[['Title', 'Genre', 'Rating', 'Link']].sort_values(by='Rating', ascending=False).head(top_n)

# 6. Streamlit 页面设置
st.set_page_config(page_title="Anime Recommender", layout="wide")

# 7. 自然语言推荐
def parse_user_query(query):
    query = query.strip()

    # 模糊匹配动漫标题
    best_match, score, _ = process.extractOne(query, df['Title'])
    if score > 80:  # 匹配度阈值
        return "title", best_match

    # 从 Genre 中匹配关键词
    genres_list = set(" ".join(df['Genre']).lower().split())
    keywords = re.findall(r'\w+', query.lower())
    matched_keywords = [k for k in keywords if k in genres_list]
    if matched_keywords:
        return "keyword", matched_keywords[0]

    return None, None

# 初始化 session_state
if 'recommended_count' not in st.session_state:
    st.session_state.recommended_count = 6
if 'filter_hentai' not in st.session_state:
    st.session_state.filter_hentai = True

# 页面导航
st.sidebar.title("选择页面")
page = st.sidebar.radio("页面", ("首页", "关键词推荐", "自然语言推荐", "设置"))

# 设置页面
if page == "设置":
    st.title("⚙️ 设置")
    st.write("自定义推荐数量和是否过滤 Hentai 类型")

    recommended_count = st.slider("每次推荐数量", min_value=3, max_value=21, value=st.session_state.recommended_count, step=3)
    st.session_state.recommended_count = recommended_count

    filter_hentai = st.checkbox("过滤 Hentai 类型动漫", value=st.session_state.filter_hentai)
    st.session_state.filter_hentai = filter_hentai

# 首页推荐
elif page == "首页":
    st.title("🎯 Anime Recommender System")
    st.write("选择你喜欢的动漫，系统会推荐相似的作品（按评分排序）")

    anime_list = df['Title'].dropna().unique()
    selected_anime = st.selectbox("选择动漫", anime_list)

    if st.button("推荐"):
        results = recommend(
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
                        st.markdown(f"**[{row['Title']}]({row['Link']})**")
                        st.write(f"⭐ {row['Rating']}")
                        st.caption(row['Genre'])
                st.markdown("<br><br>", unsafe_allow_html=True)

# 关键词推荐
elif page == "关键词推荐":
    st.title("🔍 基于关键词的动漫推荐")
    st.write("输入你喜欢的类型或主题，我们将推荐相关动漫")

    keyword = st.text_input("输入关键词", "Action")

    if st.button("推荐"):
        results = recommend_by_keyword(
            keyword,
            top_n=st.session_state.get('recommended_count', 6),
            filter_hentai=st.session_state.get('filter_hentai', True)
        )

        if results.empty:
            st.warning("没有找到相关的动漫")
        else:
            for row_start in range(0, len(results), 3):
                cols = st.columns(3, gap="large")
                for col, (_, row) in zip(cols, results.iloc[row_start:row_start + 3].iterrows()):
                    with col:
                        img_url = get_cover_image(row['Link'])
                        if img_url:
                            st.image(img_url, width=150)
                        st.markdown(f"**[{row['Title']}]({row['Link']})**")
                        st.write(f"⭐ {row['Rating']}")
                        st.caption(row['Genre'])
                st.markdown("<br><br>", unsafe_allow_html=True)

elif page == "自然语言推荐":
    st.title("🗣 自然语言动漫推荐")
    st.write("你可以用语言输入，比如 `Toradora` 或者 `I want anime with ghost`")

    user_query = st.text_input("输入一句话", "Can I having some things like Toradora")

    if st.button("搜索"):
        mode, value = parse_user_query(user_query)

        if mode == "title":
            st.info(f"检测到你想找和 **{value}** 类似的动漫")
            results = recommend(
                value,
                top_n=st.session_state.get('recommended_count', 6),
                filter_hentai=st.session_state.get('filter_hentai', True)
            )
        elif mode == "keyword":
            st.info(f"检测到你想找包含 **{value}** 类型的动漫")
            results = recommend_by_keyword(
                value,
                top_n=st.session_state.get('recommended_count', 6),
                filter_hentai=st.session_state.get('filter_hentai', True)
            )
        else:
            st.warning("无法理解你的请求，请尝试换个说法")
            results = pd.DataFrame()

        # 显示结果
        if not results.empty:
            for row_start in range(0, len(results), 3):
                cols = st.columns(3, gap="large")
                for col, (_, row) in zip(cols, results.iloc[row_start:row_start + 3].iterrows()):
                    with col:
                        img_url = get_cover_image(row['Link'])
                        if img_url:
                            st.image(img_url, width=150)
                        st.markdown(f"**[{row['Title']}]({row['Link']})**")
                        st.write(f"⭐ {row['Rating']}")
                        st.caption(row['Genre'])
                st.markdown("<br><br>", unsafe_allow_html=True)
