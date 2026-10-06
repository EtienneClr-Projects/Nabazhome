from __future__ import annotations

from datetime import datetime, timezone

from nabazhome_luckfox.domain.alarm import AlarmSchedule
from nabazhome_luckfox.infrastructure.database import DatabaseManager


class AlarmRepository:
    def __init__(self, database: DatabaseManager | None = None) -> None:
        self.database = database or DatabaseManager()

    def save(self, alarm: AlarmSchedule) -> AlarmSchedule:
        if self.database is None:
            return alarm
        self.database.connection.execute(
            """
            INSERT OR REPLACE INTO alarms (id, name, trigger_at, enabled, recurring)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                alarm.id,
                alarm.name,
                alarm.trigger_at.isoformat() if alarm.trigger_at is not None else None,
                1 if alarm.enabled else 0,
                1 if alarm.recurring else 0,
            ),
        )
        self.database.connection.commit()
        return alarm

    def list_all(self) -> list[AlarmSchedule]:
        if self.database is None:
            return []
        rows = self.database.connection.execute(
            "SELECT * FROM alarms ORDER BY trigger_at ASC"
        ).fetchall()
        alarms: list[AlarmSchedule] = []
        for row in rows:
            trigger_ts = row["trigger_at"]
            parsed_trigger = datetime.fromisoformat(trigger_ts) if trigger_ts else None
            if parsed_trigger is not None and parsed_trigger.tzinfo is not None:
                parsed_trigger = parsed_trigger.replace(tzinfo=None)
            alarms.append(
                AlarmSchedule(
                    id=row["id"],
                    name=row["name"],
                    trigger_at=parsed_trigger,
                    enabled=bool(row["enabled"]),
                    recurring=bool(row["recurring"]),
                )
            )
        return alarms

    def delete(self, alarm_id: str) -> None:
        if self.database is None:
            return
        self.database.connection.execute("DELETE FROM alarms WHERE id = ?", (alarm_id,))
        self.database.connection.commit()
