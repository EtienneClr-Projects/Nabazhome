import unittest
from datetime import datetime

from nabazhome_luckfox.services.calendar_service import CalendarService


class FakeList:
    def __init__(self, response):
        self.response = response

    def execute(self):
        return self.response


class FakeEvents:
    def __init__(self, response):
        self.response = response

    def list(self, **kwargs):
        return FakeList(self.response)


class FakeCalendarClient:
    def __init__(self, response):
        self.response = response

    def events(self):
        return FakeEvents(self.response)


class CalendarServiceTests(unittest.TestCase):
    def test_refresh_returns_upcoming_google_events(self):
        response = {
            "items": [{
                "id": "evt-1",
                "summary": "Team meeting",
                "start": {"dateTime": "2026-10-06T09:00:00+02:00"},
                "end": {"dateTime": "2026-10-06T10:00:00+02:00"},
            }]
        }
        service = CalendarService(
            enabled=True,
            calendar_id="primary",
            client_factory=lambda: FakeCalendarClient(response),
        )

        events = service.refresh()

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].summary, "Team meeting")
        self.assertEqual(events[0].start_time.isoformat(), "2026-10-06T09:00:00+02:00")

    def test_refresh_returns_empty_list_when_disabled(self):
        service = CalendarService(enabled=False)

        self.assertEqual(service.refresh(), [])


if __name__ == "__main__":
    unittest.main()
