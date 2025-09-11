import streamlit as st
from session.data_session import *
from data.data_loader import load_data
from streamlit_scroll_to_top import scroll_to_here

scroll_to_here(0, key="top")

st.title("Main Page")

session_state_format()
st.session_state.where_page = "main_page"
session_check_where()

df_animes, df_reviews = load_data()

st.markdown("### <u>Anime in the Era of Globalization</u>", unsafe_allow_html=True)

st.write(
    """
    Anime has become a global phenomenon, captivating audiences across different countries, cultures, and age groups. 
    With the growth of digital platforms, streaming services such as **Netflix**, **Crunchyroll**, and **Funimation** 
    now offer thousands of titles, making anime more accessible than ever.

    However, this abundance of choice also creates new challenges for viewers:

    - **Overwhelming options**: With so many anime available, browsing through entire catalogs can be time-consuming 
      and overwhelming.
    - **Decision fatigue**: Finding something that truly matches a viewer’s personal taste can be difficult, and many 
      users struggle to decide what to watch next.
    - **Genre complexity**: Many anime fall into multiple genres, which can confuse users when trying to pick based on 
      mood or preference. For example, the popular title *Kimetsu no Yaiba (Demon Slayer)* is tagged as *Action, Demons, 
      Historical, Shounen,* and *Supernatural*. With five different genres, it becomes harder for viewers to know if it 
      aligns with what they want to watch at that moment.

    This project aims to make anime discovery easier, helping users navigate the vast library of titles and find shows 
    that truly fit their interests.
    """
)

st.markdown("<b>From Galaxy Group</b>", unsafe_allow_html=True)
