import pandas as pd
import ast
import streamlit as st

@st.cache_data
def load_data(path="../Anime_data.csv"):
    df = pd.read_csv(path)
    df['Genre'] = df['Genre'].apply(lambda x: ' '.join(ast.literal_eval(x))
                                    if pd.notnull(x)
                                    else '')
    
    df = df.drop_duplicates(subset='Title', keep='first').reset_index(drop=True)

    return df