# all'inizio del file pages/home_page.py
import streamlit as st
from utils.auth import require_login
require_login()

# poi il resto del file come prima
import pandas as pd
import mock_store as store

def tasklist_page():
    st.header("Tasklist (cose da fare)")
    rows = []
    for e in store.list_events():
        eid = e["id"]
        base = {"Evento": f"{e['type']} - {e.get('artist_or_format_name','')} ({e.get('date','')})", "ID": eid}
        # Regole
        if e.get("hotel_status","In Sospeso") == "In Sospeso":
            rows.append({**base, "Task": "Hotel in sospeso", "Dettagli": e.get("hotel_note","")})
        if not e.get("tour_manager_id"):
            rows.append({**base, "Task": "Tour Manager da assegnare", "Dettagli": ""})
        if not e.get("van"):
            rows.append({**base, "Task": "Prenotare Van", "Dettagli": ""})
        if not e.get("viaggi"):
            rows.append({**base, "Task": "Organizzare Viaggi", "Dettagli": e.get("viaggi_note","")})
        if e.get("type") == "Format":
            if not e.get("mascotte"):
                rows.append({**base, "Task": "Mascotte da definire", "Dettagli": e.get("mascotte_note","")})
            if not e.get("allestimenti_note"):
                rows.append({**base, "Task": "Allestimenti da definire", "Dettagli": ""})
    df = pd.DataFrame(rows)
    if df.empty:
        st.success("Nessun task in sospeso. Ottimo!")
        return
    st.dataframe(df)
