import streamlit as st
import pandas as pd
import mock_store as store

def service_form(existing_id=None):
    st.subheader("Scheda service")
    svc = store.get_service(existing_id) if existing_id else {}
    name = st.text_input("Nome", value=svc.get("name",""))
    contact_name = st.text_input("Referente", value=(svc.get("contact", {}).get("name","")))
    contact_email = st.text_input("Email", value=(svc.get("contact", {}).get("email","")))
    contact_phone = st.text_input("Telefono", value=(svc.get("contact", {}).get("phone","")))
    capabilities = st.multiselect("Capacità", ["audio","luci","stage","video"], default=svc.get("capabilities", []))
    blackout_str = "\n".join([r["date"] for r in svc.get("availability_rules", []) if r.get("type")=="blackout"])
    blackout = st.text_area("Date non disponibili (YYYY-MM-DD, una per riga)", value=blackout_str)

    if st.button("Salva service"):
        payload = {
            "name": name,
            "contact": {"name": contact_name, "email": contact_email, "phone": contact_phone},
            "capabilities": capabilities,
            "availability_rules": [{"type":"blackout","date": d.strip()} for d in blackout.splitlines() if d.strip()]
        }
        sid = store.save_service(payload, existing_id)
        st.success(f"Service salvato ({sid})")

def services_list():
    svcs = store.list_services()
    df = pd.DataFrame(svcs) if svcs else pd.DataFrame(columns=["id","name","capabilities"])
    st.dataframe(df[["name","capabilities","id"]])

    ids = df["id"].tolist()
    selected = st.selectbox("Modifica service", options=["—"] + ids)
    if selected != "—":
        service_form(existing_id=selected)

def service_history_view():
    st.subheader("Storico eventi per service")
    svcs = store.list_services()
    if not svcs:
        st.info("Nessun service creato.")
        return
    names = {s["name"]: s["id"] for s in svcs}
    sel = st.selectbox("Seleziona service", options=list(names.keys()))
    sid = names[sel]
    rows = []
    for e in store.list_events():
        if e.get("service_id") == sid:
            rows.append({"date": e["date"], "location": e.get("location"), "event_id": e["id"]})
    df = pd.DataFrame(rows).sort_values("date") if rows else pd.DataFrame(columns=["date","location","event_id"])
    st.dataframe(df)
