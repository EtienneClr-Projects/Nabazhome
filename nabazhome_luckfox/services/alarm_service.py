from __future__ import annotations

from datetime import datetime, timedelta, timezone

from nabazhome_luckfox.domain.alarm import AlarmSchedule
from nabazhome_luckfox.infrastructure.database import DatabaseManager
from nabazhome_luckfox.repositories.alarm_repository import AlarmRepository


class AlarmService:
    """Business logic for alarm management."""

    @staticmethod
    def _normalize_datetime(value: datetime) -> datetime:
        if value.tzinfo is not None:
            value = value.astimezone().replace(tzinfo=None)
        return value

    def __init__(self, database: DatabaseManager | None = None) -> None:
        self.database = database
        self.repository = AlarmRepository(database) if database is not None else None
        self.current_alarm: AlarmSchedule | None = None
        self._load_latest_alarm()

    def _load_latest_alarm(self) -> None:
        if self.repository is None:
            return
        saved_alarms = self.repository.list_all()
        if saved_alarms:
            self.current_alarm = saved_alarms[-1]

    def get_active_alarm(self) -> AlarmSchedule | None:
        if self.current_alarm is None and self.repository is not None:
            self._load_latest_alarm()
        return self.current_alarm

    def list_alarms(self) -> list[AlarmSchedule]:
        if self.repository is None:
            return [self.current_alarm] if self.current_alarm is not None else []
        alarms = self.repository.list_all()
        self.current_alarm = alarms[-1] if alarms else None
        return alarms

    def set_alarm(self, trigger_at: datetime, name: str = "wake") -> AlarmSchedule:
        normalized = self._normalize_datetime(trigger_at)
        if normalized <= datetime.now():
            normalized = normalized + timedelta(days=1)

        alarm = AlarmSchedule(
            id=f"alarm-{normalized.strftime('%Y%m%d%H%M%S')}",
            name=name,
            trigger_at=normalized,
            enabled=True,
            recurring=True,
        )
        self.current_alarm = alarm
        if self.repository is not None:
            self.repository.save(alarm)
        return alarm

    def clear_alarm(self) -> None:
        self.current_alarm = None
        if self.repository is not None:
            for alarm in self.repository.list_all():
                self.repository.delete(alarm.id)

    def disable_alarm(self) -> bool:
        alarm = self.get_active_alarm()
        if alarm is None:
            return False
        alarm.enabled = False
        self.current_alarm = alarm
        if self.repository is not None:
            self.repository.save(alarm)
        return True

    def disable_ringing_alarm(self, now: datetime | None = None) -> bool:
        alarm = self.get_active_alarm()
        if alarm is None:
            return False

        current_time = self._normalize_datetime(now or datetime.now())
        target_time = self._normalize_datetime(alarm.trigger_at)
        if target_time <= current_time:
            next_day = target_time + timedelta(days=1)
            alarm.trigger_at = next_day
            alarm.enabled = True
            self.current_alarm = alarm
            if self.repository is not None:
                self.repository.save(alarm)
            return True

        alarm.enabled = False
        self.current_alarm = alarm
        if self.repository is not None:
            self.repository.save(alarm)
        return True

    def enable_alarm(self) -> bool:
        alarm = self.get_active_alarm()
        if alarm is None:
            return False
        alarm.enabled = True
        self.current_alarm = alarm
        if self.repository is not None:
            self.repository.save(alarm)
        return True

    def is_due(self, alarm: AlarmSchedule | None = None, now: datetime | None = None) -> bool:
        target = alarm or self.get_active_alarm()
        if target is None or not target.enabled or target.trigger_at is None:
            return False

        current_time = self._normalize_datetime(now or datetime.now())
        trigger_time = self._normalize_datetime(target.trigger_at)
        return current_time >= trigger_time

    def should_warn_one_hour_before(self, alarm: AlarmSchedule | None = None, now: datetime | None = None) -> bool:
        target = alarm or self.get_active_alarm()
        if target is None or not target.enabled or target.trigger_at is None:
            return False

        current_time = self._normalize_datetime(now or datetime.now())
        trigger_time = self._normalize_datetime(target.trigger_at)
        warning_time = trigger_time.replace(hour=trigger_time.hour - 1) if trigger_time.hour >= 1 else trigger_time
        return current_time >= warning_time
