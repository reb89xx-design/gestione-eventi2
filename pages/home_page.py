import streamlit as st
from utils.events_utils import home_table

def render_home():
    st.title("Home")
    q = st.text_input("Cerca artista o format")
    df = home_table(filter_artist=q if q else None)
    st.markdown(f"**{len(df)} eventi trovati**")
    if df.empty:
        st.info("Nessun evento da mostrare.")
    else:
        st.dataframe(df, height=500)
