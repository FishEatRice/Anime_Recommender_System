import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast

def content_based_filtering_recommend(df_animes, user_input):
    
    # Data Cleaning
    df_animes['synopsis'] = df_animes['synopsis'].fillna("")
    df_animes['genre'] = df_animes['genre'].fillna("")

    animes = df_animes[['uid', 'title', 'synopsis', 'genre', 'link', 'score']].copy()


    # Build dynamic genre list
    unique_genres = set()
    for g_list in animes['genre'].dropna():
        try:
            for g in ast.literal_eval(g_list):
                unique_genres.add(g.lower())
        except:
            pass

    def parse_genre(x):
        try:
            return " ".join(ast.literal_eval(x)).lower() if isinstance(x, str) else ""
        except:
            return ""

    animes['content'] = animes['synopsis'].str.lower() + " " + animes['genre'].apply(parse_genre)

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(animes['content'])

    query = user_input.lower()
    matched = False

    #Multi-genre check
    matched_genres = [g for g in unique_genres if g in query]

    if matched_genres:
        results = animes[animes['genre'].apply(
            lambda x: all(mg in x.lower() for mg in matched_genres)
        )]
        matched = True

    if not matched:
        #Fallback to TF-IDF similarity
        query_vec = vectorizer.transform([query])
        sim_scores = cosine_similarity(query_vec, tfidf_matrix).ravel()
        sorted_indices = sim_scores.argsort()[::-1]
        results = animes.iloc[sorted_indices].reset_index(drop=True)

    return results, user_input
