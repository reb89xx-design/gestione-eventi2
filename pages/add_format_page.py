# all'inizio del file pages/home_page.py
import streamlit as st
from utils.auth import require_login
require_login()

# poi il resto del file come prima
def add_format_page():
    st.header("Aggiungi Format")
    name = st.text_input("Nome format")
    description = st.text_area("Descrizione")
    note = st.text_area("Note")
    if st.button("Salva"):
        fid = store.save_format({"name": name, "description": description, "note": note})
        st.success(f"Format creato ({fid})")
