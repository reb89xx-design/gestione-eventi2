import streamlit as st
import mock_store as store

def add_tour_manager_page():
    st.header("Aggiungi Tour Manager")
    name = st.text_input("Nome")
    email = st.text_input("Email")
    phone = st.text_input("Telefono")
    note = st.text_area("Note")
    if st.button("Salva"):
        sid = store.save_tour_manager({"name": name, "email": email, "phone": phone, "note": note})
        st.success(f"Tour Manager creato ({sid})")
