import requests
from bs4 import BeautifulSoup
import streamlit as st

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
