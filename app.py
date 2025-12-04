import streamlit as st

# Configurazione della pagina principale
st.set_page_config(page_title="Gestione Eventi", layout="wide")

# Menu laterale per navigare tra le sezioni
st.sidebar.title("Navigazione")
page = st.sidebar.radio("Vai a:", ["Dashboard Eventi", "Gestione Service", "Calendario"])

# Routing verso le pagine
if page == "Dashboard Eventi":
    from pages.events_page import events_page
    events_page()

elif page == "Gestione Service":
    from pages.services_page import services_page
    services_page()

elif page == "Calendario":
    from pages.calendar_page import calendar_page
    calendar_page()
