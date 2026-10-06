from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class DeviceState:
    online: bool = True
    status: str = "ready"
    last_sync: datetime | None = None
    requested_status: str | None = None


class DeviceService:
    def __init__(self) -> None:
        self.state = DeviceState(last_sync=datetime.now(timezone.utc))

    def initialize(self) -> None:
        self.state = DeviceState(
            online=True,
            status="ready",
            last_sync=datetime.now(timezone.utc),
            requested_status="ready",
        )

    def get_status(self) -> DeviceState:
        return self.state

    def set_status(self, status: str = "ready") -> DeviceState:
        self.state.status = status
        self.state.online = status not in {"booting", "offline"}
        self.state.last_sync = datetime.now(timezone.utc)
        self.state.requested_status = status
        return self.state
