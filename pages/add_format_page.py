import streamlit as st
import mock_store as store

def add_format_page():
    st.header("Aggiungi Format")
    name = st.text_input("Nome format")
    description = st.text_area("Descrizione")
    note = st.text_area("Note")
    if st.button("Salva"):
        fid = store.save_format({"name": name, "description": description, "note": note})
        st.success(f"Format creato ({fid})")
