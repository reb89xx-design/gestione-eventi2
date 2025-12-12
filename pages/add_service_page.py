# all'inizio del file pages/home_page.py
import streamlit as st
from utils.auth import require_login
require_login()

# poi il resto del file come prima
def add_service_page():
    st.header("Aggiungi Service")
    name = st.text_input("Nome")
    contact_name = st.text_input("Referente")
    contact_email = st.text_input("Email")
    contact_phone = st.text_input("Telefono")
    capabilities = st.multiselect("Capacità", ["audio","luci","stage","video"])
    blackout = st.text_area("Date non disponibili (YYYY-MM-DD, una per riga)")
    if st.button("Salva"):
        payload = {
            "name": name,
            "contact": {"name": contact_name, "email": contact_email, "phone": contact_phone},
            "capabilities": capabilities,
            "availability_rules": [{"type":"blackout","date": d.strip()} for d in blackout.splitlines() if d.strip()]
        }
        sid = store.save_service(payload)
        st.success(f"Service creato ({sid})")
