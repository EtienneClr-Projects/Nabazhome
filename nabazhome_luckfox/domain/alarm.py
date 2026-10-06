from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AlarmSchedule:
    id: str = "alarm-0"
    name: str = "wake"
    trigger_at: datetime | None = None
    enabled: bool = True
    recurring: bool = True
