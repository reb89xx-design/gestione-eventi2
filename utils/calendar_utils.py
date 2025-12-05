import streamlit as st
import pandas as pd
from datetime import timedelta
import mock_store as store
from utils.events_utils import event_form

def fetch_events_range(d_from, d_to):
    df = pd.DataFrame(store.list_events())
    if df.empty: return df
    return df[(df["date"] >= d_from.isoformat()) & (df["date"] <= d_to.isoformat())].sort_values("date")

def weekly_view(start_date):
    days = [start_date + timedelta(days=i) for i in range(7)]
    df = fetch_events_range(days[0], days[-1])
    st.subheader(f"Settimana: {days[0].isoformat()} — {days[-1].isoformat()}")
    for d in days:
        st.markdown(f"### {d.strftime('%A %d/%m/%Y')}")
        day_df = df[df["date"] == d.isoformat()]
        for _, r in day_df.iterrows():
            if st.button(f"Apri evento {r['id']}", key=f"open_{r['id']}"):
                st.session_state["editing_event"] = r["id"]
        if "editing_event" in st.session_state and st.session_state["editing_event"]:
            event_form(existing_id=st.session_state["editing_event"])
            st.session_state["editing_event"] = None

def monthly_view(month_start):
    month_end = (month_start.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    df = fetch_events_range(month_start, month_end)
    st.subheader(f"Mese: {month_start.strftime('%B %Y')}")
    if df.empty:
        st.info("Nessun evento per questo mese.")
        return
    # Griglia giorni
    for d in pd.date_range(month_start, month_end):
        d_iso = d.date().isoformat()
        day_df = df[df["date"] == d_iso]
        st.markdown(f"### {d.strftime('%A %d/%m/%Y')}")
        if day_df.empty:
            st.write("—")
        else:
            for _, r in day_df.iterrows():
                cols = st.columns([3,1])
                with cols[0]:
                    st.write(f"{r['type']} • {r.get('artist_or_format_name','')} • {r.get('location','')}")
                with cols[1]:
                    if st.button("Apri", key=f"open_month_{r['id']}"):
                        st.session_state["editing_event"] = r["id"]
            if "editing_event" in st.session_state and st.session_state["editing_event"]:
                st.markdown("---")
                event_form(existing_id=st.session_state["editing_event"])
                st.session_state["editing_event"] = None
