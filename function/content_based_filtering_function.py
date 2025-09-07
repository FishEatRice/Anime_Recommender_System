import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast

def content_based_filtering_recommend(df_animes, user_input):
    # Cleaning null values
    df_animes['synopsis'] = df_animes['synopsis'].fillna("")
    df_animes['genre'] = df_animes['genre'].fillna("")

    animes = df_animes[['uid', 'title', 'synopsis', 'genre', 'link', 'score']].copy()

    def parse_genre(x):
        try:
            return " ".join(ast.literal_eval(x)) if isinstance(x, str) else ""
        except:
            return ""
    animes['content'] = animes['synopsis'] + " " + animes['genre'].apply(parse_genre)

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(animes['content'])

    query_vec = vectorizer.transform([user_input])
    sim_scores = cosine_similarity(query_vec, tfidf_matrix).ravel()

    sorted_indices = sim_scores.argsort()[::-1]

    results = animes.iloc[sorted_indices].reset_index(drop=True)

    return results, user_input
