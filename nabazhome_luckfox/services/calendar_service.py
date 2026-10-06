from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class CalendarEvent:
    id: str
    summary: str
    start_time: datetime | None = None
    end_time: datetime | None = None


class CalendarService:
    def refresh(self) -> list[CalendarEvent]:
        return []
