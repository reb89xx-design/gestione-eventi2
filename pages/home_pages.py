import streamlit as st
from utils.events_utils import home_table

def home_page():
    st.header("Home")
    colf, colbtn = st.columns([3,1])
    with colf:
        filter_artist = st.text_input("Filtro Artisti (ricerca per nome)")
    with colbtn:
        if st.button("AGGIUNGI NUOVO EVENTO"):
            st.session_state["nav_override"] = "Aggiungi Evento"
            st.experimental_rerun()
    df = home_table(filter_artist=filter_artist)
    st.dataframe(df)
