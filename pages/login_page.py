# pages/login_page.py
import streamlit as st
from utils.auth import login

def render_login():
    st.set_page_config(page_title="Login", layout="centered")
    st.title("Accedi a Gestione Eventi")
    st.write("Inserisci le credenziali per continuare")

    col1, col2 = st.columns([2,1])
    with col1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
    with col2:
        if st.button("Accedi"):
            user = login(email.strip(), password)
            if user:
                st.session_state["user"] = user
                st.success(f"Benvenuto {user.get('name','')}")
                # se c'è una pagina richiesta, ricarica per navigare lì
                next_page = st.session_state.pop("next_page", None)
                if next_page:
                    st.experimental_rerun()
                else:
                    st.experimental_rerun()
            else:
                st.error("Credenziali non valide")
    st.markdown("---")
    st.write("Account di test: admin@example.com / admin")
