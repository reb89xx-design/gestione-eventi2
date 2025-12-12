import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import mock_store as store
from utils.events_utils import generate_readable_event_id, is_service_available

st.set_page_config(page_title="Calendario", layout="wide")

def _status_color(status: str) -> str:
    return {"confirmed":"#2ecc71","draft":"#f1c40f","cancelled":"#e74c3c"}.get(status,"#95a5a6")

@st.cache_data
def load_all_events():
    df = pd.DataFrame(store.list_events())
    if df.empty:
        return df
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    else:
        df["date"] = None
    return df

@st.cache_data
def load_lookup(name):
    mapping = {
        "services": store.list_services,
        "tms": store.list_tour_managers,
        "artists": store.list_artists,
        "formats": store.list_formats
    }
    return mapping[name]()

if "cal_month" not in st.session_state:
    st.session_state.cal_month = date.today().replace(day=1)
if "editing_event" not in st.session_state:
    st.session_state.editing_event = None

col1, col2, col3 = st.columns([1,3,1])
with col1:
    if st.button("◀"):
        m = st.session_state.cal_month
        st.session_state.cal_month = (m.replace(day=1) - timedelta(days=1)).replace(day=1)
with col2:
    st.markdown(f"### {st.session_state.cal_month.strftime('%B %Y')}")
with col3:
    if st.button("▶"):
        m = st.session_state.cal_month
        next_month = (m.replace(day=28) + timedelta(days=4)).replace(day=1)
        st.session_state.cal_month = next_month
    if st.button("Oggi"):
        st.session_state.cal_month = date.today().replace(day=1)

with st.sidebar:
    st.header("Filtri")
    services = load_lookup("services")
    tms = load_lookup("tms")
    artists = load_lookup("artists")
    formats = load_lookup("formats")
    sel_service = st.selectbox("Service", options=["Tutti"] + [s["name"] for s in services])
    sel_tm = st.selectbox("Tour Manager", options=["Tutti"] + [t["name"] for t in tms])
    sel_type = st.selectbox("Tipo", options=["Tutti","Artist","Format"])
    sel_status = st.selectbox("Stato", options=["Tutti","confirmed","draft","cancelled"])

df_all = load_all_events()
df = df_all.copy()
if sel_service != "Tutti":
    df = df[df["service_id"].notna() & df["service_id"].apply(lambda sid: any(s["id"]==sid and s["name"]==sel_service for s in services))]
if sel_tm != "Tutti":
    df = df[df["tour_manager_id"].notna() & df["tour_manager_id"].apply(lambda tid: any(t["id"]==tid and t["name"]==sel_tm for t in tms))]
if sel_type != "Tutti":
    df = df[df["type"]==sel_type]
if sel_status != "Tutti":
    df = df[df["status"]==sel_status]

month_start = st.session_state.cal_month
month_end = (month_start.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
start_calendar = month_start - timedelta(days=month_start.weekday())
end_calendar = month_end + timedelta(days=(6 - month_end.weekday()))
days = pd.date_range(start_calendar, end_calendar).to_pydatetime().tolist()

for week_start in range(0, len(days), 7):
    cols = st.columns(7)
    for i in range(7):
        d = days[week_start + i].date()
        col = cols[i]
        with col:
            is_current_month = (d.month == month_start.month)
            header_style = "font-weight:600;" if is_current_month else "color:#9aa0a6;"
            st.markdown(f"<div style='{header_style}'>{d.strftime('%a %d')}</div>", unsafe_allow_html=True)
            day_events = df[df["date"] == d]
            count = len(day_events)
            st.markdown(f"**{count}**")
            if st.button("+", key=f"create_{d.isoformat()}"):
                st.session_state.editing_event = {"id": None, "date": d.isoformat()}
            if count > 0:
                preview = day_events.head(3)
                for _, r in preview.iterrows():
                    color = _status_color(r.get("status",""))
                    label = f"{r.get('type','')} • {r.get('artist_or_format_name','')} • {r.get('location','')}"
                    st.markdown(
                        f"<div style='display:flex;justify-content:space-between;align-items:center;padding:2px 0'>"
                        f"<div style='flex:1'>{label}</div>"
                        f"<div style='background:{color};width:10px;height:10px;border-radius:50%'></div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                    if st.button("Apri", key=f"open_{r['id']}"):
                        st.session_state.editing_event = r.to_dict()
                if count > 3:
                    if st.button(f"Mostra tutti ({count})", key=f"all_{d.isoformat()}"):
                        with st.expander(f"Eventi del {d.strftime('%A %d/%m/%Y')}"):
                            for _, r in day_events.iterrows():
                                st.write(f"- {r.get('type','')} • {r.get('artist_or_format_name','')} • {r.get('location','')}")
                                if st.button("Apri", key=f"open_full_{r['id']}"):
                                    st.session_state.editing_event = r.to_dict()

if st.session_state.editing_event:
    ev = st.session_state.editing_event
    with st.modal("Evento"):
        st.markdown("### Dettagli evento")
        ev_type = st.selectbox("Tipo", options=["Artist","Format"], index=0 if not ev.get("type") else (0 if ev["type"]=="Artist" else 1))
        ev_date = st.date_input("Data", value=datetime.fromisoformat(ev["date"]).date() if ev.get("date") else date.today())
        ev_location = st.text_input("Luogo", value=ev.get("location",""))
        ev_name = st.text_input("Artista o Format", value=ev.get("artist_or_format_name",""))
        ev_service = st.selectbox("Service", options=[""] + [s["id"] for s in services], index=0)
        ev_tm = st.selectbox("Tour Manager", options=[""] + [t["id"] for t in tms], index=0)
        ev_status = st.selectbox("Stato", options=["draft","confirmed","cancelled"], index=0)
        ev_notes = st.text_area("Note", value=ev.get("note",""), height=120)

        col_save, col_cancel = st.columns([1,1])
        with col_cancel:
            if st.button("Annulla"):
                st.session_state.editing_event = None
                st.experimental_rerun()
        with col_save:
            if st.button("Salva"):
                payload = {
                    "type": ev_type,
                    "date": ev_date.isoformat(),
                    "location": ev_location,
                    "artist_or_format_name": ev_name,
                    "service_id": ev_service or None,
                    "tour_manager_id": ev_tm or None,
                    "status": ev_status,
                    "note": ev_notes
                }
                if not ev.get("id"):
                    payload["id"] = generate_readable_event_id(payload["type"], payload["date"], payload["location"])
                else:
                    payload["id"] = ev["id"]
                if payload.get("service_id") and not is_service_available(payload["service_id"], payload["date"]):
                    st.warning("Service non disponibile in questa data.")
                else:
                    store.save_event(payload)
                    st.success("Evento salvato")
                    st.cache_data.clear()
                    st.session_state.editing_event = None
                    st.experimental_rerun()
