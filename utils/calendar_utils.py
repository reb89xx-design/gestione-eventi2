import pandas as pd
from datetime import date, timedelta
import mock_store as store

def events_in_range(start_date: date, end_date: date) -> pd.DataFrame:
    df = pd.DataFrame(store.list_events())
    if df.empty:
        return df
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    else:
        df["date"] = None
    return df[(df["date"] >= start_date) & (df["date"] <= end_date)].copy()
