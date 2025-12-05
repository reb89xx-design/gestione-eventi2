import json, os, uuid, shutil

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
FILES = {
    "events": os.path.join(DATA_DIR, "events.json"),
    "services": os.path.join(DATA_DIR, "services.json"),
    "tour_managers": os.path.join(DATA_DIR, "tour_managers.json"),
    "artists": os.path.join(DATA_DIR, "artists.json"),
    "formats": os.path.join(DATA_DIR, "formats.json"),
}
ATTACH_DIR = os.path.join(DATA_DIR, "attachments")

def _ensure_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(ATTACH_DIR, exist_ok=True)
    for _, path in FILES.items():
        if not os.path.exists(path):
            with open(path, "w") as f: json.dump([], f)
_ensure_files()

def _load(name):
    with open(FILES[name]) as f: return json.load(f)
def _save(name, data):
    with open(FILES[name], "w") as f: json.dump(data, f, indent=2)

# CRUD generici
def list_events(): return _load("events")
def list_services(): return _load("services")
def list_tour_managers(): return _load("tour_managers")
def list_artists(): return _load("artists")
def list_formats(): return _load("formats")

def save_event(payload, event_id=None):
    items = list_events()
    if not event_id:
        event_id = str(uuid.uuid4())
        payload["id"] = event_id
        items.append(payload)
    else:
        found = False
        for i, e in enumerate(items):
            if e["id"] == event_id:
                payload["id"] = event_id
                items[i] = payload
                found = True
                break
        if not found:
            payload["id"] = event_id
            items.append(payload)
    _save("events", items)
    return event_id

def get_event(event_id):
    return next((e for e in list_events() if e["id"] == event_id), None)

def save_service(payload, service_id=None):
    items = list_services()
    if not service_id:
        service_id = str(uuid.uuid4())
        payload["id"] = service_id
        items.append(payload)
    else:
        for i, s in enumerate(items):
            if s["id"] == service_id:
                payload["id"] = service_id
                items[i] = payload
                break
        else:
            payload["id"] = service_id
            items.append(payload)
    _save("services", items)
    return service_id

def save_tour_manager(payload, tm_id=None):
    items = list_tour_managers()
    if not tm_id:
        tm_id = str(uuid.uuid4())
        payload["id"] = tm_id
        items.append(payload)
    else:
        for i, s in enumerate(items):
            if s["id"] == tm_id:
                payload["id"] = tm_id
                items[i] = payload
                break
        else:
            payload["id"] = tm_id
            items.append(payload)
    _save("tour_managers", items)
    return tm_id

def save_artist(payload, artist_id=None):
    items = list_artists()
    if not artist_id:
        artist_id = str(uuid.uuid4())
        payload["id"] = artist_id
        items.append(payload)
    else:
        for i, s in enumerate(items):
            if s["id"] == artist_id:
                payload["id"] = artist_id
                items[i] = payload
                break
        else:
            payload["id"] = artist_id
            items.append(payload)
    _save("artists", items)
    return artist_id

def save_format(payload, format_id=None):
    items = list_formats()
    if not format_id:
        format_id = str(uuid.uuid4())
        payload["id"] = format_id
        items.append(payload)
    else:
        for i, s in enumerate(items):
            if s["id"] == format_id:
                payload["id"] = format_id
                items[i] = payload
                break
        else:
            payload["id"] = format_id
            items.append(payload)
    _save("formats", items)
    return format_id

def save_attachment(streamlit_file, event_id):
    filename = streamlit_file.name
    target_dir = os.path.join(ATTACH_DIR, event_id or "temp")
    os.makedirs(target_dir, exist_ok=True)
    path = os.path.join(target_dir, filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(streamlit_file, f)
    return {"name": filename, "storage_path": path, "type": "attachment"}
