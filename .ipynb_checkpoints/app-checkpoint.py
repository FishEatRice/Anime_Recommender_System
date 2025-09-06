import streamlit as st
import pandas as pd
import numpy as np

# ---- Sidebar Navigation ----
st.sidebar.title("🎬 Anime Recommender System")
page = st.sidebar.radio("Choose a module:", 
                        ["Collaborative Filtering", 
                         "Content-Based Filtering", 
                         "Evaluation Metrics"])

# ---- Collaborative Filtering ----
if page == "Collaborative Filtering":
    st.title("👥 Collaborative Filtering Recommender")

    # Example: user input
    user_id = st.text_input("Enter User ID", "U1")

    if st.button("Get Recommendations"):
        # TODO: replace with your collaborative filtering function
        recommendations = ["Anime A", "Anime B", "Anime C"]
        st.write("### Recommended for", user_id)
        st.write(recommendations)

# ---- Content-Based Filtering ----
elif page == "Content-Based Filtering":
    st.title("📚 Content-Based Filtering Recommender")

    # Example: anime selection
    anime_title = st.text_input("Enter an anime title", "Naruto")

    if st.button("Recommend Similar"):
        # TODO: replace with your content-based function
        recommendations = ["Bleach", "One Piece", "Fairy Tail"]
        st.write("### Similar to", anime_title)
        st.write(recommendations)

# ---- Evaluation Metrics ----
elif page == "Evaluation Metrics":
    st.title("📊 Evaluation Metrics")

    # Example: precision, recall, F1
    y_true = [1, 0, 1, 1, 0]
    y_pred = [1, 0, 0, 1, 1]

    from sklearn.metrics import precision_score, recall_score, f1_score

    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    st.write(f"**Precision:** {precision:.2f}")
    st.write(f"**Recall:** {recall:.2f}")
    st.write(f"**F1 Score:** {f1:.2f}")
