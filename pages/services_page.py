# all'inizio del file pages/home_page.py
import streamlit as st
from utils.auth import require_login
require_login()

# poi il resto del file come prima
from utils.services_utils import services_list, service_form, service_history_view

def services_page():
    st.header("Gestione service")
    services_list()
    st.divider()
    st.subheader("Nuovo service")
    service_form()
    st.divider()
    service_history_view()

