import streamlit as st
from utils.services_utils import services_list, service_form, service_history_view

def services_page():
    st.header("Gestione service")
    services_list()
    st.divider()
    st.subheader("Nuovo service")
    service_form()
    st.divider()
    service_history_view()
