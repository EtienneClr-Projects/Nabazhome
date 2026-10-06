from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from pathlib import Path
from urllib.parse import parse_qs

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from nabazhome_luckfox.config.settings import Settings
from nabazhome_luckfox.infrastructure.database import DatabaseManager
from nabazhome_luckfox.services.alarm_service import AlarmService
from nabazhome_luckfox.services.board_service import BoardService
from nabazhome_luckfox.services.calendar_service import CalendarService
from nabazhome_luckfox.services.device_service import DeviceService
from nabazhome_luckfox.services.notification_service import NotificationService
from nabazhome_luckfox.services.weather_service import WeatherService


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    logger = logging.getLogger("nabazhome.alarm")
    app = FastAPI(title=settings.app_name)
    dashboard_path = Path(__file__).resolve().parent.parent / "dashboard"
    app.mount("/static", StaticFiles(directory=str(dashboard_path)), name="static")
    device_service = DeviceService()
    device_service.initialize()
    board_service = BoardService()
    database = DatabaseManager(settings.db_path)
    alarm_service = AlarmService(database=database)
    app.state.alarm_service = alarm_service
    app.state.device_service = device_service
    weather_service = WeatherService(
        latitude=settings.weather_latitude,
        longitude=settings.weather_longitude,
        api_key=settings.weather_api_key,
    )
    calendar_service = CalendarService()
    notification_service = NotificationService()

    @app.get("/")
    def index() -> FileResponse:
        dashboard_file = dashboard_path / "index.html"
        return FileResponse(dashboard_file)

    @app.on_event("shutdown")
    def close_database() -> None:
        database.close()

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "app": settings.app_name,
            "device": device_service.get_status().status,
        }

    @app.get("/api/status")
    def status() -> dict[str, Any]:
        state = device_service.get_status()
        return {
            "online": state.online,
            "status": state.status,
            "last_sync": state.last_sync.isoformat() if state.last_sync else None,
        }

    @app.get("/status")
    def legacy_status() -> dict[str, Any]:
        return status()

    @app.post("/status")
    def set_status(status: str = "ready") -> dict[str, Any]:
        device_service.set_status(status)
        current = device_service.get_status()
        return {
            "online": current.online,
            "status": current.status,
            "requested_status": current.status,
        }

    @app.get("/api/dashboard")
    def dashboard() -> dict[str, Any]:
        device = device_service.get_status()
        weather = weather_service.fetch_snapshot()
        active_alarm = alarm_service.get_active_alarm()
        ringing = bool(active_alarm is not None and active_alarm.enabled and alarm_service.is_due(active_alarm))
        if ringing:
            logger.info("Alarm due: %s at %s", active_alarm.name if active_alarm else "unknown", active_alarm.trigger_at.isoformat() if active_alarm and active_alarm.trigger_at else "unknown")
            device_service.set_status("alerting")
            device = device_service.get_status()
        elif active_alarm is None or not active_alarm.enabled:
            device_service.set_status("ready")
            device = device_service.get_status()
        alarms = []
        if active_alarm is not None and active_alarm.enabled:
            alarms = [{
                "id": active_alarm.id,
                "name": active_alarm.name,
                "trigger_at": active_alarm.trigger_at.isoformat() if active_alarm.trigger_at else None,
                "enabled": active_alarm.enabled,
            }]

        events = calendar_service.refresh()
        return {
            "device": {
                "online": device.online,
                "status": device.status,
                "requested_status": device.requested_status,
                "last_sync": device.last_sync.isoformat() if device.last_sync else None,
            },
            "weather": {
                "temperature_c": weather.temperature_c,
                "feels_like_c": weather.feels_like_c,
                "condition": weather.condition,
                "precipitation_probability": weather.precipitation_probability,
            },
            "alarms": alarms,
            "ringing": ringing,
            "calendar": {
                "events": [
                    {
                        "id": event.id,
                        "summary": event.summary,
                        "start_time": event.start_time.isoformat() if event.start_time else None,
                        "end_time": event.end_time.isoformat() if event.end_time else None,
                    }
                    for event in events
                ]
            },
        }

    @app.get("/alarms")
    def get_alarms() -> dict[str, Any]:
        active_alarm = alarm_service.get_active_alarm()
        if active_alarm is None or not active_alarm.enabled:
            return {"alarms": []}
        return {"alarms": [{"id": active_alarm.id, "name": active_alarm.name, "trigger_at": active_alarm.trigger_at.isoformat() if active_alarm.trigger_at else None, "enabled": active_alarm.enabled}]}

    @app.post("/alarms")
    def create_alarm(trigger_at: str, name: str = "wake") -> dict[str, Any]:
        parsed = datetime.fromisoformat(trigger_at)
        alarm = alarm_service.set_alarm(parsed, name=name)
        return {"id": alarm.id, "name": alarm.name, "trigger_at": alarm.trigger_at.isoformat() if alarm.trigger_at else None, "enabled": alarm.enabled}

    @app.post("/alarms/disable")
    def disable_alarm() -> dict[str, Any]:
        disabled = alarm_service.disable_alarm()
        device_service.set_status("ready")
        return {"disabled": disabled, "alarms": []}

    @app.post("/alarms/disable-ringing")
    def disable_ringing_alarm() -> dict[str, Any]:
        disabled = alarm_service.disable_ringing_alarm()
        device_service.set_status("ready")
        return {"disabled": disabled, "alarms": []}

    @app.delete("/alarms")
    def delete_alarm() -> dict[str, Any]:
        return disable_alarm()

    @app.get("/weather")
    def get_weather() -> dict[str, Any]:
        snapshot = weather_service.fetch_snapshot()
        return {
            "temperature_c": snapshot.temperature_c,
            "feels_like_c": snapshot.feels_like_c,
            "condition": snapshot.condition,
            "precipitation_probability": snapshot.precipitation_probability,
        }

    @app.get("/calendar")
    def get_calendar() -> dict[str, Any]:
        events = calendar_service.refresh()
        return {
            "events": [
                {
                    "id": event.id,
                    "summary": event.summary,
                    "start_time": event.start_time.isoformat() if event.start_time else None,
                    "end_time": event.end_time.isoformat() if event.end_time else None,
                }
                for event in events
            ]
        }

    @app.post("/notifications")
    def create_notification(message: str, channel: str = "local") -> dict[str, Any]:
        notification = notification_service.send(message, channel=channel)
        board_service.announce(message)
        return {"text": notification.text, "channel": notification.channel}

    @app.post("/api/animation")
    async def trigger_animation(request: Request) -> dict[str, Any]:
        action: str | None = None
        content_type = request.headers.get("content-type", "")

        if "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
            body = await request.body()
            if body:
                parsed = parse_qs(body.decode("utf-8"), keep_blank_values=True)
                values = parsed.get("action", [])
                if values:
                    action = values[0]
        else:
            try:
                payload = await request.json()
            except Exception:
                payload = {}
            action = payload.get("action")

        if action is None:
            raise HTTPException(status_code=400, detail="Animation action is required.")

        allowed_actions = {
            "right-ear",
            "left-ear",
            "both-ears",
            "home-ears",
            "led-green",
            "led-red",
            "led-orange",
        }
        if action not in allowed_actions:
            raise HTTPException(status_code=400, detail=f"Unsupported animation action: {action}")

        return {
            "status": "queued",
            "action": action,
            "implemented": False,
            "message": "Animation command accepted; hardware execution is still pending.",
        }

    return app
