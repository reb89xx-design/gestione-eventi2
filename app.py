# app.py
import streamlit as st
from utils.auth import require_login, logout

PUBLIC_PAGES = {"Login": "login_page"}
PROTECTED_PAGES = {
    "Home": "home_page",
    "Calendario": "calendar_page",
    "Eventi": "events_page",
    "Servizi": "services_page",
    "Impostazioni": "settings_page"
}

if "page" not in st.session_state:
    st.session_state.page = "Login"

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

if st.session_state.page == "Login":
    from pages.login_page import render_login
    render_login()
else:
    require_login()
    page_module = PROTECTED_PAGES.get(st.session_state.page)
    if page_module:
        module_path = f"pages.{page_module}"
        module = __import__(module_path, fromlist=["*"])
        # prefer render_<name> then render
        candidate = "render_" + page_module.split("_")[0]
        if hasattr(module, candidate):
            getattr(module, candidate)()
        elif hasattr(module, "render"):
            module.render()
        else:
            st.warning("Pagina non ancora implementata. Aggiungi il file in pages/")
