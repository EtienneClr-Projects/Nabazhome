from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Callable

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


@dataclass
class CalendarEvent:
    id: str
    summary: str
    start_time: datetime | None = None
    end_time: datetime | None = None


class CalendarService:
    def __init__(
        self,
        enabled: bool = False,
        calendar_id: str = "primary",
        credentials_path: str | None = None,
        token_path: str | None = None,
        client_factory: Callable[[], Any] | None = None,
    ) -> None:
        self.enabled = enabled
        self.calendar_id = calendar_id or "primary"
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.client_factory = client_factory or self._default_client_factory
        self.logger = logging.getLogger("nabazhome.calendar")

    def _default_client_factory(self) -> Any:
        try:
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build
        except ImportError as exc:  # pragma: no cover - dependency is optional at runtime
            raise RuntimeError("google-api-python-client is not installed") from exc

        creds = None
        if self.token_path and os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            elif self.credentials_path and os.path.exists(self.credentials_path):
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
                if self.token_path:
                    with open(self.token_path, "w", encoding="utf-8") as token_file:
                        token_file.write(creds.to_json())
            else:
                self.logger.warning("Google Calendar is enabled but no valid credentials were found.")
                return None

        return build("calendar", "v3", credentials=creds)

    @staticmethod
    def _parse_datetime(value: str | None) -> datetime | None:
        if value is None:
            return None
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            try:
                return datetime.fromisoformat(f"{value}T00:00:00")
            except ValueError:
                return None

    def refresh(self) -> list[CalendarEvent]:
        if not self.enabled:
            return []

        try:
            client = self.client_factory()
        except Exception as exc:  # pragma: no cover - external dependency path
            self.logger.warning("Google Calendar refresh failed: %s", exc)
            return []

        if client is None:
            return []

        now = datetime.now(timezone.utc)
        window_end = now + timedelta(days=30)

        try:
            response = (
                client.events()
                .list(
                    calendarId=self.calendar_id,
                    timeMin=now.isoformat(),
                    timeMax=window_end.isoformat(),
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
        except Exception as exc:  # pragma: no cover - external API call path
            self.logger.warning("Google Calendar API call failed: %s", exc)
            return []

        events: list[CalendarEvent] = []
        for item in response.get("items", []):
            start_raw = item.get("start", {}).get("dateTime") or item.get("start", {}).get("date")
            end_raw = item.get("end", {}).get("dateTime") or item.get("end", {}).get("date")
            events.append(
                CalendarEvent(
                    id=str(item.get("id") or ""),
                    summary=str(item.get("summary") or "Untitled event"),
                    start_time=self._parse_datetime(start_raw),
                    end_time=self._parse_datetime(end_raw),
                )
            )
        return events
