# utils/auth.py
import streamlit as st
import mock_store as store
from typing import Optional

def _ensure_session():
    if "user" not in st.session_state:
        st.session_state["user"] = None

def login(email: str, password: str) -> Optional[dict]:
    """
    Verifica credenziali contro mock_store users.
    Restituisce user dict se ok, None altrimenti.
    """
    users = store.list_users()
    for u in users:
        if u.get("email") == email and u.get("password") == password:
            return u
    return None

def require_login():
    """
    Se l'utente non è loggato, salva la pagina richiesta e mostra la pagina di login.
    Import lazy di pages.login_page per evitare import circolare.
    """
    _ensure_session()
    if not st.session_state.get("user"):
        st.session_state["next_page"] = st.session_state.get("requested_page", None)
        # import locale per evitare import circolare
        from pages.login_page import render_login
        render_login()
        st.stop()

def logout():
    st.session_state["user"] = None
