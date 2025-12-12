# app.py
import streamlit as st
from utils.auth import require_login, logout

st.set_page_config(page_title="Gestione Eventi", layout="wide")

# Pagine disponibili e label
PUBLIC_PAGES = {"Login": "login_page"}
PROTECTED_PAGES = {
    "Home": "home_page",
    "Calendario": "calendar_page",
    "Eventi": "events_page",        # placeholder
    "Servizi": "services_page",     # placeholder
    "Impostazioni": "settings_page" # placeholder
}

# inizializza stato
if "page" not in st.session_state:
    st.session_state.page = "Login"

# se utente loggato, mostra logout e menu protetto
user = st.session_state.get("user")
if user:
    st.sidebar.write(f"**{user.get('name','Utente')}**")
    if st.sidebar.button("Logout"):
        logout()
        st.experimental_rerun()
    page = st.sidebar.selectbox("Vai a", list(PROTECTED_PAGES.keys()))
    st.session_state.page = page
else:
    page = st.sidebar.selectbox("Vai a", list(PUBLIC_PAGES.keys()))
    st.session_state.page = page

# routing semplice
if st.session_state.page == "Login":
    from pages.login_page import render_login
    render_login()
else:
    # richiede login prima di importare la pagina protetta
    require_login()
    # import dinamico della pagina selezionata
    page_module = PROTECTED_PAGES.get(st.session_state.page)
    if page_module:
        module_path = f"pages.{page_module}"
        module = __import__(module_path, fromlist=["*"])
        # ogni pagina espone render_<name> o render
        if hasattr(module, "render_" + page_module.split("_")[0]):
            getattr(module, "render_" + page_module.split("_")[0])()
        elif hasattr(module, "render"):
            module.render()
        else:
            # fallback: se la pagina non esiste ancora, mostra placeholder
            st.warning("Pagina non ancora implementata. Aggiungi il file in pages/")
