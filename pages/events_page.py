import streamlit as st
from utils.events_utils import events_table, event_form

def events_page():
    st.header("Dashboard eventi")
    events_table()
    st.divider()
    st.subheader("Nuovo evento")
    event_form()
