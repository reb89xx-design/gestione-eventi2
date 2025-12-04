import json, os, uuid, shutil
from datetime import date

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
EVENTS_FILE = os.path.join(DATA_DIR, "events.json")
SERVICES_FILE = os.path.join(DATA_DIR, "services.json")
ATTACH_DIR = os.path.join(DATA_DIR, "attachments")

def _ensure_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(ATTACH_DIR, exist_ok=True)
    if not os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, "w") as f: json.dump([], f)
    if not os.path.exists(SERVICES_FILE):
        with open(SERVICES_FILE, "w") as f: json.dump([], f)

_ensure_files()

# --- Events ---
def list_events():
    with open(EVENTS_FILE) as f:
        return json.load(f)

def save_event(payload, event_id=None):
    events = list_events()
    if event_id is None:
        event_id = str(uuid.uuid4())
        payload["id"] = event_id
        events.append(payload)
    else:
        for i, e in enumerate(events):
            if e["id"] == event_id:
                payload["id"] = event_id
                events[i] = payload
                break
        else:
            payload["id"] = event_id
            events.append(payload)
    with open(EVENTS_FILE, "w") as f: json.dump(events, f, indent=2)
    return event_id

def get_event(event_id):
    return next((e for e in list_events() if e["id"] == event_id), None)

# --- Services ---
def list_services():
    with open(SERVICES_FILE) as f:
        return json.load(f)

def save_service(payload, service_id=None):
    services = list_services()
    if service_id is None:
        service_id = str(uuid.uuid4())
        payload["id"] = service_id
        services.append(payload)
    else:
        for i, s in enumerate(services):
            if s["id"] == service_id:
                payload["id"] = service_id
                services[i] = payload
                break
        else:
            payload["id"] = service_id
            services.append(payload)
    with open(SERVICES_FILE, "w") as f: json.dump(services, f, indent=2)
    return service_id

def get_service(service_id):
    return next((s for s in list_services() if s["id"] == service_id), None)

# --- Attachments ---
def save_attachment(streamlit_file, event_id):
    filename = streamlit_file.name
    target_dir = os.path.join(ATTACH_DIR, event_id)
    os.makedirs(target_dir, exist_ok=True)
    path = os.path.join(target_dir, filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(streamlit_file, f)
    return {"name": filename, "storage_path": path, "type": "attachment"}
