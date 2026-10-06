import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from nabazhome_luckfox.domain.alarm import AlarmSchedule
from nabazhome_luckfox.infrastructure.database import DatabaseManager
from nabazhome_luckfox.services.alarm_service import AlarmService


class AlarmServiceTests(unittest.TestCase):
    def test_alarm_is_due_when_triggered_in_the_past(self):
        service = AlarmService()
        now = datetime(2026, 10, 5, 8, 0, 0)
        alarm = AlarmSchedule(trigger_at=now - timedelta(minutes=5))

        self.assertTrue(service.is_due(alarm, now))

    def test_alarm_is_not_due_before_trigger_time(self):
        service = AlarmService()
        now = datetime(2026, 10, 5, 8, 0, 0)
        alarm = AlarmSchedule(trigger_at=now + timedelta(minutes=5))

        self.assertFalse(service.is_due(alarm, now))

    def test_set_alarm_creates_alarm_schedule(self):
        service = AlarmService()
        alarm = service.set_alarm(datetime(2026, 10, 5, 9, 30, 0))

        self.assertIsNotNone(alarm)
        self.assertEqual(alarm.trigger_at.hour, 9)
        self.assertEqual(alarm.trigger_at.minute, 30)

    def test_set_alarm_persists_and_loads_from_database(self):
        db_path = Path(tempfile.mkdtemp()) / 'alarm-test.db'
        database = DatabaseManager(db_path)
        service = AlarmService(database=database)
        alarm_time = datetime(2026, 10, 5, 9, 30, 0)

        created = service.set_alarm(alarm_time, name='Wake-up')
        reloaded = service.get_active_alarm()

        self.assertEqual(created.id, reloaded.id)
        self.assertEqual(reloaded.name, 'Wake-up')
        self.assertEqual(reloaded.trigger_at, alarm_time)

        database.close()

    def test_alarm_persists_after_restart(self):
        db_path = Path(tempfile.mkdtemp()) / 'restart-alarm.db'
        first_db = DatabaseManager(db_path)
        first_service = AlarmService(database=first_db)
        alarm_time = datetime(2026, 10, 5, 9, 30, 0)

        first_service.set_alarm(alarm_time, name='Wake-up')
        first_db.close()

        reopened = AlarmService(database=DatabaseManager(db_path))
        reloaded = reopened.get_active_alarm()

        self.assertIsNotNone(reloaded)
        self.assertEqual(reloaded.name, 'Wake-up')
        self.assertEqual(reloaded.trigger_at, alarm_time)
        self.assertTrue(reloaded.enabled)

    def test_disabled_alarm_is_not_due(self):
        service = AlarmService()
        now = datetime(2026, 10, 5, 8, 0, 0)
        alarm = AlarmSchedule(trigger_at=now - timedelta(minutes=5), enabled=False)

        self.assertFalse(service.is_due(alarm, now))


if __name__ == "__main__":
    unittest.main()
