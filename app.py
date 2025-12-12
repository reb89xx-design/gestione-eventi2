import streamlit as st

st.set_page_config(page_title="Gestione Eventi", layout="wide")
st.title("Gestione Eventi")

st.sidebar.title("Menu")
page = st.sidebar.selectbox("Vai a", ["Home", "Calendario"])

if page == "Home":
    from pages.home_page import render_home
    render_home()
else:
    from pages.calendar_page import render_calendar
    render_calendar()
