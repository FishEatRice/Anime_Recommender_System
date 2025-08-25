from fuzzywuzzy import process
import re

def parse_user_query(query, df):
    query = query.strip()
    best_match, score, _ = process.extractOne(query, df['Title'])
    if score > 80:
        return "title", best_match

    genres_list = set(" ".join(df['Genre']).lower().split())
    keywords = re.findall(r'\w+', query.lower())
    matched_keywords = [k for k in keywords if k in genres_list]
    if matched_keywords:
        return "keyword", matched_keywords[0]

    return None, None
