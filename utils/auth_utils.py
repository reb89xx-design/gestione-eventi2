import streamlit as st
import json, os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")

def _ensure_users():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(USERS_FILE):
        # utente admin di default: pass "admin"
        seed = [{"name": "Admin", "email": "admin@example.com", "role": "admin", "password": "admin"}]
        with open(USERS_FILE, "w") as f: json.dump(seed, f, indent=2)
_ensure_users()

def _load_users():
    with open(USERS_FILE) as f: return json.load(f)

def _save_users(users):
    with open(USERS_FILE, "w") as f: json.dump(users, f, indent=2)

def require_login():
    if "user" in st.session_state and st.session_state["user"]:
        return
    st.title("Accedi")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        users = _load_users()
        u = next((x for x in users if x["email"] == email and x["password"] == password), None)
        if u:
            st.session_state["user"] = {"name": u["name"], "email": u["email"], "role": u["role"]}
            st.success("Login effettuato")
            st.experimental_rerun()
        else:
            st.error("Credenziali non valide")

def current_user():
    return st.session_state.get("user", {})

def users_admin_page():
    st.header("Gestione utenti")
    users = _load_users()
    st.write("Utenti registrati:")
    st.dataframe(users)
    st.subheader("Aggiungi utente")
    name = st.text_input("Nome")
    email = st.text_input("Email")
    role = st.selectbox("Ruolo", ["admin","segretaria","tour_manager"])
    password = st.text_input("Password", type="password")
    if st.button("Crea utente"):
        users.append({"name": name, "email": email, "role": role, "password": password})
        _save_users(users)
        st.success("Utente creato")
