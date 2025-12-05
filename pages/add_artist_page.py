import streamlit as st
import mock_store as store

def add_artist_page():
    st.header("Aggiungi Artista")
    name = st.text_input("Nome artista")
    genre = st.text_input("Genere")
    note = st.text_area("Note")
    if st.button("Salva"):
        aid = store.save_artist({"name": name, "genre": genre, "note": note})
        st.success(f"Artista creato ({aid})")
