from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Notification:
    text: str
    channel: str = "local"


class NotificationService:
    def send(self, message: str, channel: str = "local") -> Notification:
        return Notification(text=message, channel=channel)
