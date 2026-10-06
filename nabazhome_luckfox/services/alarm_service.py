from __future__ import annotations

from datetime import datetime

from nabazhome_luckfox.domain.alarm import AlarmSchedule
from nabazhome_luckfox.infrastructure.database import DatabaseManager
from nabazhome_luckfox.repositories.alarm_repository import AlarmRepository


class AlarmService:
    """Business logic for alarm management."""

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
        alarm = AlarmSchedule(
            id=f"alarm-{trigger_at.strftime('%Y%m%d%H%M%S')}",
            name=name,
            trigger_at=trigger_at,
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

    def is_due(self, alarm: AlarmSchedule | None = None, now: datetime | None = None) -> bool:
        target = alarm or self.get_active_alarm()
        if target is None or target.trigger_at is None:
            return False

        current_time = now or datetime.utcnow()
        return current_time >= target.trigger_at

    def should_warn_one_hour_before(self, alarm: AlarmSchedule | None = None, now: datetime | None = None) -> bool:
        target = alarm or self.get_active_alarm()
        if target is None or target.trigger_at is None:
            return False

        current_time = now or datetime.utcnow()
        warning_time = target.trigger_at.replace(hour=target.trigger_at.hour - 1) if target.trigger_at.hour >= 1 else target.trigger_at
        return current_time >= warning_time
