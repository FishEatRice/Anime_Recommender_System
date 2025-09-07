import streamlit as st

pages = {
    "🏠Main": [st.Page("pages/main_page.py", title="Main Page")],
    "🕵️Collaborative-Filtering": [
        st.Page("pages/item_based_filtering_page.py", title="Item-Based Collaborative Filtering"),
        st.Page("pages/user_based_filtering_page.py", title="User-Based Collaborative Filtering"),
    ],
    "🔍Content-Filtering": [
        st.Page("pages/content_based_filtering_page.py", title="Content-Based Collaborative Filtering"),
    ],
    "📊Evaluation Metrics": [
        st.Page("pages/Precision_Recall_F1_page.py", title="Precision & Recall & F1 Value"),
        st.Page("pages/MSE_page.py", title="MSE & RMSE Value"),
    ],
    "⚙️Settings": [st.Page("pages/settings_page.py", title="Settings Page")],
}

pg = st.navigation(pages)
pg.run()

st.Page("pages/main_page.py", title="Main Page")