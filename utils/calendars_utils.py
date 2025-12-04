import streamlit as st
import pandas as pd
from datetime import timedelta
import mock_store as store

def fetch_events_range(d_from, d_to):
    df = pd.DataFrame(store.list_events())
    if df.empty:
        return df
    return df[(df["date"] >= d_from.isoformat()) & (df["date"] <= d_to.isoformat())]

def weekly_view(start_date):
    days = [start_date + timedelta(days=i) for i in range(7)]
    df = fetch_events_range(days[0], days[-1])
    st.subheader(f"Settimana: {days[0].isoformat()} — {days[-1].isoformat()}")
    for d in days:
        st.markdown(f"### {d.strftime('%A %d/%m/%Y')}")
        day_df = df[df["date"] == d.isoformat()]
        for _, r in day_df.iterrows():
            st.markdown(f"- **Evento:** {r['id']} — **Orario:** {r['start_time']}–{r['end_time']} — **Location:** {r.get('location','')} — **Service:** {r.get('service_id','—')}")

def monthly_view(month_start):
    month_end = (month_start.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    df = fetch_events_range(month_start, month_end)
    st.subheader(f"Mese: {month_start.strftime('%B %Y')}")
    if df.empty:
        st.info("Nessun evento per questo mese.")
        return
    agg = df.groupby("date").agg({"id":"count"}).rename(columns={"id":"eventi"}).reset_index()
    st.dataframe(agg)
    for d in pd.date_range(month_start, month_end):
        d_iso = d.date().isoformat()
        day_df = df[df["date"] == d_iso]
        if not day_df.empty:
            st.markdown(f"### {d.strftime('%A %d/%m/%Y')}")
            for _, r in day_df.iterrows():
                st.markdown(f"- **Evento:** {r['id']} — **Orario:** {r['start_time']}–{r['end_time']} — **Location:** {r.get('location','')} — **Service:** {r.get('service_id','—')}")
