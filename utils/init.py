# rende utils un package Python
# file vuoto o con export utili
from .events_utils import (
    generate_readable_event_id,
    is_service_available,
    check_service_conflict,
    home_table,
)
__all__ = [
    "generate_readable_event_id",
    "is_service_available",
    "check_service_conflict",
    "home_table",
]
