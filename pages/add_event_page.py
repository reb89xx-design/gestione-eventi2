import streamlit as st
from utils.events_utils import event_form

def add_event_page():
    st.header("Aggiungi Evento")
    event_form()
