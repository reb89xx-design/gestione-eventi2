import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import mock_store as store

def check_service_conflict(service_id, event_date, exclude_event_id=None):
    if not service_id: return []
    conflicts = []
    for e in store.list_events():
        if e.get("service_id") == service_id and e.get("date") == event_date:
            if exclude_event_id and e.get("id") == exclude_event_id: continue
            conflicts.append(e["id"])
    return conflicts

def is_service_available(service_id, ev_date):
    svc = store.get_service(service_id)
    if not svc: return True
    blackout = {r.get("date") for r in svc.get("availability_rules", []) if r.get("type") == "blackout"}
    return ev_date not in blackout

def list_events_df():
    rows = store.list_events()
    return pd.DataFrame(rows) if rows else pd.DataFrame(columns=["id","date","location","start_time","end_time","service_id"])

def event_form(existing_id=None):
    st.subheader("Scheda evento")
    ev = store.get_event(existing_id) if existing_id else {}
    col1, col2 = st.columns(2)
    with col1:
        ev_date = st.date_input("Data", value=(datetime.strptime(ev["date"], "%Y-%m-%d").date() if ev.get("date") else date.today()))
        start_time = st.time_input("Orario inizio", value=(datetime.strptime(ev["start_time"], "%H:%M").time() if ev.get("start_time") else datetime.now().time()))
        end_time = st.time_input("Orario fine", value=(datetime.strptime(ev["end_time"], "%H:%M").time() if ev.get("end_time") else (datetime.now() + timedelta(hours=2)).time()))
        location = st.text_input("Location", value=ev.get("location",""))
    with col2:
        services = store.list_services()
        names = ["— Nessuno —"] + [s["name"] for s in services]
        default_name = "— Nessuno —"
        if ev.get("service_id"):
            match = next((s["name"] for s in services if s["id"] == ev["service_id"]), None)
            if match: default_name = match
        selected = st.selectbox("Service assegnato", options=names, index=names.index(default_name))
        service_id = None if selected == "— Nessuno —" else next(s["id"] for s in services if s["name"] == selected)
        artists = st.text_input("Artisti/Format (separati da virgola)", value=",".join(ev.get("artists", [])))

    st.markdown("**Documenti allegati**")
    uploaded_files = st.file_uploader("Contratti/Rider tecnico ecc.", accept_multiple_files=True)
    docs_meta = ev.get("documents", [])
    if uploaded_files:
        for f in uploaded_files:
            docs_meta.append(store.save_attachment(f, existing_id or "temp"))

    if st.button("Salva evento"):
        if end_time <= start_time:
            st.error("Orario fine deve essere successivo all'inizio.")
            return
        payload = {
            "date": ev_date.isoformat(),
            "start_time": start_time.strftime("%H:%M"),
            "end_time": end_time.strftime("%H:%M"),
            "location": location,
            "artists": [a.strip() for a in artists.split(",")] if artists else [],
            "service_id": service_id,
            "documents": docs_meta,
            "status": "confirmed"
        }
        if service_id:
            if not is_service_available(service_id, payload["date"]):
                st.error("Il service è indisponibile in quella data (blackout).")
                return
            conflicts = check_service_conflict(service_id, payload["date"], exclude_event_id=existing_id)
            if conflicts:
                st.error(f"Conflitto: il service è già assegnato agli eventi {conflicts} nello stesso giorno.")
                return
        ev_id = store.save_event(payload, existing_id)
        st.success(f"Evento salvato ({ev_id})")

def events_table():
    df = list_events_df()
    st.dataframe(df[["date","location","start_time","end_time","service_id","id"]])
    ids = df["id"].tolist()
    selected = st.selectbox("Modifica evento", options=["—"] + ids) if ids else "—"
    if selected != "—":
        event_form(existing_id=selected)
    elif df.empty:
        st.info("Nessun evento. Crea il primo qui sotto.")
