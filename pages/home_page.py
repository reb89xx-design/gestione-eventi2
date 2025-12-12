import streamlit as st
import pandas as pd
from utils.events_utils import home_table

st.set_page_config(page_title="Home", layout="wide")

st.title("Home - Gestione Eventi")

# filtro rapido
q = st.text_input("Cerca artista o format")

df = home_table(filter_artist=q if q else None)
st.markdown(f"**{len(df)} eventi trovati**")

if df.empty:
    st.info("Nessun evento da mostrare.")
else:
    st.dataframe(df, height=400)

