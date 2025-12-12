import streamlit as st

st.set_page_config(page_title="Gestione Eventi", layout="wide")
st.title("Gestione Eventi")

st.markdown("Usa la sidebar per navigare tra le pagine: Home e Calendario.")
st.sidebar.title("Menu")
page = st.sidebar.selectbox("Vai a", ["Home", "Calendario"])

if page == "Home":
    from pages.home_page import *
else:
    from pages.Calendar import *
