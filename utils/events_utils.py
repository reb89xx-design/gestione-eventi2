import streamlit as st
import pandas as pd
from datetime import date
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
    svc = next((s for s in store.list_services() if s["id"] == service_id), None)
    if not svc: return True
    blackout = {r.get("date") for r in svc.get("availability_rules", []) if r.get("type") == "blackout"}
    return ev_date not in blackout

def home_table(filter_artist=None):
    df = pd.DataFrame(store.list_events())
    if df.empty:
        return pd.DataFrame(columns=["id","type","date","location","artist_or_format","service_id","hotel_status"])
    if filter_artist:
        df = df[df["artist_or_format_name"].str.contains(filter_artist, case=False, na=False)]
    df = df.sort_values("date")
    return df[["id","type","date","location","artist_or_format_name","service_id","hotel_status"]]

def event_form(existing_id=None):
    st.subheader("Scheda evento")
    ev = store.get_event(existing_id) if existing_id else {}
    # Tipo: Artista o Format
    event_type = st.radio("Tipo evento", ["Artista","Format"], index=(0 if ev.get("type","Artista")=="Artista" else 1), horizontal=True)

    # Campi condivisi
    ev_date = st.date_input("Data", value=(date.fromisoformat(ev["date"]) if ev.get("date") else date.today()))
    location = st.text_input("Luogo", value=ev.get("location",""))

    services = store.list_services()
    svc_names = ["— Nessuno —"] + [s["name"] for s in services]
    current_svc_name = "— Nessuno —"
    if ev.get("service_id"):
        match = next((s["name"] for s in services if s["id"] == ev["service_id"]), None)
        if match: current_svc_name = match
    svc_sel = st.selectbox("Service", options=svc_names, index=svc_names.index(current_svc_name))
    service_id = None if svc_sel == "— Nessuno —" else next(s["id"] for s in services if s["name"] == svc_sel)

    hotel_status = st.selectbox("Hotel", ["Prenotato","In Sospeso"], index=(["Prenotato","In Sospeso"].index(ev.get("hotel_status","In Sospeso")) if ev.get("hotel_status") else 1))
    hotel_note = st.text_input("Note hotel", value=ev.get("hotel_note",""))

    facchini = st.text_input("Facchini", value=ev.get("facchini",""))
    promoter = st.text_input("Promoter", value=ev.get("promoter",""))

    # Tour manager
    tms = store.list_tour_managers()
    tm_names = ["— Nessuno —"] + [t["name"] for t in tms]
    current_tm = "— Nessuno —"
    if ev.get("tour_manager_id"):
        match = next((t["name"] for t in tms if t["id"] == ev["tour_manager_id"]), None)
        if match: current_tm = match
    tm_sel = st.selectbox("Tour Manager", options=tm_names, index=tm_names.index(current_tm))
    tour_manager_id = None if tm_sel == "— Nessuno —" else next(t["id"] for t in tms if t["name"] == tm_sel)

    viaggi = st.text_input("Viaggi", value=ev.get("viaggi",""))
    viaggi_note = st.text_area("Note viaggi", value=ev.get("viaggi_note",""))
    note_aggiuntive = st.text_area("Note aggiuntive", value=ev.get("note_aggiuntive",""))

    # Pagamenti
    colp1, colp2 = st.columns(2)
    with colp1:
        acconto = st.text_input("Acconto", value=ev.get("acconto",""))
    with colp2:
        saldo = st.text_input("Saldo", value=ev.get("saldo",""))
    van = st.text_input("Van", value=ev.get("van",""))

    # Specifici per tipo
    artist_or_format_id = None
    artist_or_format_name = ""
    if event_type == "Artista":
        artists = store.list_artists()
        art_names = ["— Seleziona —"] + [a["name"] for a in artists]
        sel = st.selectbox("Artista", options=art_names, index=art_names.index(ev.get("artist_or_format_name","— Seleziona —")) if ev.get("artist_or_format_name") else 0)
        if sel != "— Seleziona —":
            artist_or_format_id = next(a["id"] for a in artists if a["name"] == sel)
            artist_or_format_name = sel
    else:
        formats = store.list_formats()
        fmt_names = ["— Seleziona —"] + [f["name"] for f in formats]
        sel = st.selectbox("Format", options=fmt_names, index=fmt_names.index(ev.get("artist_or_format_name","— Seleziona —")) if ev.get("artist_or_format_name") else 0)
        if sel != "— Seleziona —":
            artist_or_format_id = next(f["id"] for f in formats if f["name"] == sel)
            artist_or_format_name = sel
        # campi extra per Format
        mascotte = st.text_input("Mascotte", value=ev.get("mascotte",""))
        mascotte_note = st.text_area("Note Mascotte", value=ev.get("mascotte_note",""))
        allestimenti_note = st.text_area("Allestimenti (Note)", value=ev.get("allestimenti_note",""))

    # Allegati
    st.markdown("**Documenti allegati**")
    uploaded_files = st.file_uploader("Contratti / rider tecnico", accept_multiple_files=True)
    docs_meta = ev.get("documents", [])
    if uploaded_files:
        for f in uploaded_files:
            docs_meta.append(store.save_attachment(f, existing_id or "temp"))

    if st.button("Salva evento"):
        payload = {
            "type": event_type,
            "date": ev_date.isoformat(),
            "location": location,
            "service_id": service_id,
            "hotel_status": hotel_status,
            "hotel_note": hotel_note,
            "facchini": facchini,
            "promoter": promoter,
            "tour_manager_id": tour_manager_id,
            "viaggi": viaggi,
            "viaggi_note": viaggi_note,
            "note_aggiuntive": note_aggiuntive,
            "acconto": acconto,
            "saldo": saldo,
            "van": van,
            "artist_or_format_id": artist_or_format_id,
            "artist_or_format_name": artist_or_format_name,
            "documents": docs_meta,
            "status": "confirmed"
        }
        # Extra campi per Format
        if event_type == "Format":
            payload.update({
                "mascotte": locals().get("mascotte",""),
                "mascotte_note": locals().get("mascotte_note",""),
                "allestimenti_note": locals().get("allestimenti_note","")
            })
        # vincoli service
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
        st.experimental_rerun()
