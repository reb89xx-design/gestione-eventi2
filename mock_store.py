import os
import json
import uuid
import shutil
from typing import List, Dict, Any, Optional, Union

# Percorso alla cartella data (assume mock_store.py nella root del repo)
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
ATTACH_DIR = os.path.join(DATA_DIR, "attachments")

FILES = {
    "events": os.path.join(DATA_DIR, "events.json"),
    "services": os.path.join(DATA_DIR, "services.json"),
    "tour_managers": os.path.join(DATA_DIR, "tour_managers.json"),
    "artists": os.path.join(DATA_DIR, "artists.json"),
    "formats": os.path.join(DATA_DIR, "formats.json"),
    "users": os.path.join(DATA_DIR, "users.json"),
}

# --- Utility per file I/O ---

def _ensure_dirs_and_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(ATTACH_DIR, exist_ok=True)
    for key, path in FILES.items():
        if not os.path.exists(path):
            # seed minimo: users con admin, gli altri array vuoti
            if key == "users":
                seed = [
                    {"name": "Admin", "email": "admin@example.com", "role": "admin", "password": "admin"}
                ]
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(seed, f, indent=2, ensure_ascii=False)
            else:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=2, ensure_ascii=False)

# Chiama all'import per garantire file esistenti
_ensure_dirs_and_files()

def _read(name: str) -> List[Dict[str, Any]]:
    path = FILES[name]
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def _write(name: str, data: List[Dict[str, Any]]) -> None:
    path = FILES[name]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# --- Listing / retrieval ---

def list_events() -> List[Dict[str, Any]]:
    return _read("events")

def list_services() -> List[Dict[str, Any]]:
    return _read("services")

def list_tour_managers() -> List[Dict[str, Any]]:
    return _read("tour_managers")

def list_artists() -> List[Dict[str, Any]]:
    return _read("artists")

def list_formats() -> List[Dict[str, Any]]:
    return _read("formats")

def list_users() -> List[Dict[str, Any]]:
    return _read("users")

def get_event(event_id: str) -> Optional[Dict[str, Any]]:
    return next((e for e in list_events() if e.get("id") == event_id), None)

def get_service(service_id: str) -> Optional[Dict[str, Any]]:
    return next((s for s in list_services() if s.get("id") == service_id), None)

# --- Save / update helpers ---

def _upsert(items: List[Dict[str, Any]], payload: Dict[str, Any], id_field: str = "id") -> str:
    if id_field in payload and payload.get(id_field):
        # update if exists
        for i, it in enumerate(items):
            if it.get(id_field) == payload[id_field]:
                items[i] = payload
                return payload[id_field]
        # not found -> append
        items.append(payload)
        return payload[id_field]
    else:
        new_id = str(uuid.uuid4())
        payload[id_field] = new_id
        items.append(payload)
        return new_id

# --- CRUD specifici ---

def save_event(payload: Dict[str, Any], event_id: Optional[str] = None) -> str:
    events = list_events()
    if event_id:
        payload["id"] = event_id
    eid = _upsert(events, payload, "id")
    _write("events", events)
    return eid

def delete_event(event_id: str) -> bool:
    events = list_events()
    new = [e for e in events if e.get("id") != event_id]
    if len(new) == len(events):
        return False
    _write("events", new)
    # rimuovi eventuali allegati
    attach_path = os.path.join(ATTACH_DIR, event_id)
    if os.path.exists(attach_path):
        shutil.rmtree(attach_path, ignore_errors=True)
    return True

def save_service(payload: Dict[str, Any], service_id: Optional[str] = None) -> str:
    services = list_services()
    if service_id:
        payload["id"] = service_id
    sid = _upsert(services, payload, "id")
    _write("services", services)
    return sid

def save_tour_manager(payload: Dict[str, Any], tm_id: Optional[str] = None) -> str:
    tms = list_tour_managers()
    if tm_id:
        payload["id"] = tm_id
    tid = _upsert(tms, payload, "id")
    _write("tour_managers", tms)
    return tid

def save_artist(payload: Dict[str, Any], artist_id: Optional[str] = None) -> str:
    artists = list_artists()
    if artist_id:
        payload["id"] = artist_id
    aid = _upsert(artists, payload, "id")
    _write("artists", artists)
    return aid

def save_format(payload: Dict[str, Any], format_id: Optional[str] = None) -> str:
    fmts = list_formats()
    if format_id:
        payload["id"] = format_id
    fid = _upsert(fmts, payload, "id")
    _write("formats", fmts)
    return fid

def save_user(payload: Dict[str, Any], user_email: Optional[str] = None) -> str:
    users = list_users()
    # use email as unique key if provided
    if user_email:
        payload["email"] = user_email
    # if email exists update
    for i, u in enumerate(users):
        if u.get("email") == payload.get("email"):
            users[i] = payload
            _write("users", users)
            return payload["email"]
    users.append(payload)
    _write("users", users)
    return payload.get("email", str(uuid.uuid4()))

# --- Attachments ---

def _ensure_event_attach_dir(event_id: str) -> str:
    target = os.path.join(ATTACH_DIR, event_id)
    os.makedirs(target, exist_ok=True)
    return target

def save_attachment(streamlit_file: Any, event_id: Optional[str]) -> Dict[str, Any]:
    """
    streamlit_file: oggetto UploadedFile di Streamlit o file-like.
    event_id: id dell'evento; se None verrà usata cartella 'temp'
    Restituisce metadata: {name, storage_path, type}
    """
    eid = event_id or "temp"
    target_dir = _ensure_event_attach_dir(eid)
    filename = getattr(streamlit_file, "name", None) or f"file_{uuid.uuid4().hex}"
    target_path = os.path.join(target_dir, filename)

    # Se è un UploadedFile di Streamlit ha metodo .read()
    try:
        # streamlit UploadedFile supports .read()
        content = streamlit_file.read()
        with open(target_path, "wb") as f:
            if isinstance(content, bytes):
                f.write(content)
            else:
                f.write(content.encode("utf-8"))
    except Exception:
        # fallback: se è file-like, usare shutil
        try:
            with open(target_path, "wb") as f:
                shutil.copyfileobj(streamlit_file, f)
        except Exception:
            # ultima risorsa: creare file vuoto
            open(target_path, "wb").close()

    return {"name": filename, "storage_path": target_path, "type": "attachment"}

def list_attachments(event_id: str) -> List[Dict[str, Any]]:
    target = os.path.join(ATTACH_DIR, event_id)
    if not os.path.exists(target):
        return []
    files = []
    for fname in os.listdir(target):
        files.append({"name": fname, "storage_path": os.path.join(target, fname)})
    return files

def delete_attachment(event_id: str, filename: str) -> bool:
    path = os.path.join(ATTACH_DIR, event_id, filename)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False

# --- Utility di ricerca / controllo ---

def find_events_by_service_and_date(service_id: str, date_iso: str) -> List[Dict[str, Any]]:
    return [e for e in list_events() if e.get("service_id") == service_id and e.get("date") == date_iso]

def find_events_by_artist_or_format(af_id: str) -> List[Dict[str, Any]]:
    return [e for e in list_events() if e.get("artist_or_format_id") == af_id]

# --- Export / import helper (facoltativo) ---

def export_all() -> Dict[str, Any]:
    return {
        "events": list_events(),
        "services": list_services(),
        "tour_managers": list_tour_managers(),
        "artists": list_artists(),
        "formats": list_formats(),
        "users": list_users(),
    }

def import_all(data: Dict[str, Any]) -> None:
    for key in ["events", "services", "tour_managers", "artists", "formats", "users"]:
        if key in data:
            _write(key, data[key])

# --- Fine mock_store ---
