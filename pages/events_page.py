# all'inizio del file pages/home_page.py
import streamlit as st
from utils.auth import require_login
require_login()

# poi il resto del file come prima
from utils.events_utils import events_table, event_form

def events_page():
    st.header("Dashboard eventi")
    events_table()
    st.divider()
    st.subheader("Nuovo evento")
    event_form()
