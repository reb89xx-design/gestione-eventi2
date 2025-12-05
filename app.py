import streamlit as st

# Configurazione della pagina principale
import streamlit as st
from utils.auth_utils import require_login, current_user

st.set_page_config(page_title="Gestione Eventi", layout="wide")

# LOGIN PAGE
require_login()

user = current_user()
st.sidebar.title(f"Benvenuto: {user.get('name','Utente')}")
st.sidebar.caption(f"Ruolo: {user['role']}")

# Navigazione
nav_items = [
    "Home",
    "Aggiungi Evento",
    "Aggiungi Service",
    "Aggiungi Tour Manager",
    "Aggiungi Artista",
    "Aggiungi Format",
    "Calendario Generale",
    "Tasklist",
    "Gestione Utenti"
]

# Limitazioni base per ruoli (admin tutto; segretaria no utenti; tour manager solo alcune)
role = user["role"]
allowed = set(nav_items)
if role == "segretaria":
    allowed.discard("Gestione Utenti")
elif role == "tour_manager":
    allowed = {"Home", "Calendario Generale", "Tasklist"}

page = st.sidebar.radio("Navigazione", sorted(list(allowed)))

if page == "Home":
    from pages.home_page import home_page
    home_page()
elif page == "Aggiungi Evento":
    from pages.add_event_page import add_event_page
    add_event_page()
elif page == "Aggiungi Service":
    from pages.add_service_page import add_service_page
    add_service_page()
elif page == "Aggiungi Tour Manager":
    from pages.add_tour_manager_page import add_tour_manager_page
    add_tour_manager_page()
elif page == "Aggiungi Artista":
    from pages.add_artist_page import add_artist_page
    add_artist_page()
elif page == "Aggiungi Format":
    from pages.add_format_page import add_format_page
    add_format_page()
elif page == "Calendario Generale":
    from pages.calendar_page import calendar_page
    calendar_page()
elif page == "Tasklist":
    from pages.tasklist_page import tasklist_page
    tasklist_page()
elif page == "Gestione Utenti":
    from utils.auth_utils import users_admin_page
    users_admin_page()
