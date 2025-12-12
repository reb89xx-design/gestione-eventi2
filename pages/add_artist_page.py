# all'inizio del file pages/home_page.py
import streamlit as st
from utils.auth import require_login
require_login()

# poi il resto del file come prima

def add_artist_page():
    st.header("Aggiungi Artista")
    name = st.text_input("Nome artista")
    genre = st.text_input("Genere")
    note = st.text_area("Note")
    if st.button("Salva"):
        aid = store.save_artist({"name": name, "genre": genre, "note": note})
        st.success(f"Artista creato ({aid})")
