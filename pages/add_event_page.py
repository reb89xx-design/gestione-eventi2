# all'inizio del file pages/home_page.py
import streamlit as st
from utils.auth import require_login
require_login()

# poi il resto del file come prima
def add_event_page():
    st.header("Aggiungi Evento")
    event_form()
