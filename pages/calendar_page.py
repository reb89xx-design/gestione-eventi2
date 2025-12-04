import streamlit as st
from utils.calendar_utils import weekly_view, monthly_view
from datetime import date, timedelta

def calendar_page():
    st.header("Calendario condiviso")
    mode = st.radio("Vista", ["Settimanale","Mensile"], horizontal=True)
    if mode == "Settimanale":
        start = st.date_input("Inizio settimana", value=date.today() - timedelta(days=date.today().weekday()))
        weekly_view(start)
    else:
        first_day = date.today().replace(day=1)
        month = st.date_input("Mese", value=first_day)
        monthly_view(month)
