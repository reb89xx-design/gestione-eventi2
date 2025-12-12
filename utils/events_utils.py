import re
from datetime import datetime
import pandas as pd
import mock_store as store
from typing import Optional, List

def _slugify(text: str, maxlen: int = 20) -> str:
    if not text:
        return "NA"
    s = text.upper()
    s = re.sub(r'[^A-Z0-9]+', '-', s)
    s = s.strip('-')
    return s[:maxlen]

def generate_readable_event_id(event_type: str, date_iso: str, location: str, suffix: str = None) -> str:
    dt = date_iso.replace('-', '') if date_iso else datetime.now().strftime("%Y%m%d")
    t = (event_type or "EV").upper()
    loc = _slugify(location or "NA", maxlen=12)
    base = f"{t}-{dt}-{loc}"
    if not suffix:
        same = [e for e in store.list_events() if e.get("id","").startswith(base)]
        idx = len(same) + 1
        suffix = f"{idx:02d}"
    return f"{base}-{suffix}"

def is_service_available(service_id: str, ev_date: str) -> bool:
    svc = next((s for s in store.list_services() if s["id"] == service_id), None)
    if not svc:
        return True
    blackout = {r.get("date") for r in svc.get("availability_rules", []) if r.get("type") == "blackout"}
    return ev_date not in blackout

def check_service_conflict(service_id: str, event_date: str, exclude_event_id: Optional[str] = None) -> List[str]:
    if not service_id:
        return []
    conflicts = []
    for e in store.list_events():
        if e.get("service_id") == service_id and e.get("date") == event_date:
            if exclude_event_id and e.get("id") == exclude_event_id:
                continue
            conflicts.append(e["id"])
    return conflicts

def home_table(filter_artist: Optional[str] = None) -> pd.DataFrame:
    df = pd.DataFrame(store.list_events())
    if df.empty:
        return pd.DataFrame(columns=["id","type","date","location","artist_or_format_name","service_id","hotel_status"])
    for col in ["artist_or_format_name","service_id","hotel_status","location","type","date","id"]:
        if col not in df.columns:
            df[col] = None
    if filter_artist:
        df = df[df["artist_or_format_name"].str.contains(filter_artist, case=False, na=False)]
    df = df.sort_values("date")
    return df[["id","type","date","location","artist_or_format_name","service_id","hotel_status"]]
