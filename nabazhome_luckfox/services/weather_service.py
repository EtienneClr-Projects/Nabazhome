from __future__ import annotations

from dataclasses import dataclass


@dataclass
class WeatherSnapshot:
    temperature_c: float | None = 18.0
    feels_like_c: float | None = 17.0
    condition: str = "clear"
    precipitation_probability: int | None = 10


class WeatherService:
    def __init__(self, latitude: float = 50.698, longitude: float = 3.177, api_key: str = "") -> None:
        self.latitude = latitude
        self.longitude = longitude
        self.api_key = api_key

    def fetch_snapshot(self) -> WeatherSnapshot:
        try:
            import requests

            url = (
                "https://api.open-meteo.com/v1/forecast"
                f"?latitude={self.latitude}&longitude={self.longitude}&current=temperature_2m,apparent_temperature,precipitation&hourly=temperature_2m,precipitation_probability&timezone=auto"
            )
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            payload = response.json()
            current = payload.get("current", {})
            if current:
                return WeatherSnapshot(
                    temperature_c=current.get("temperature_2m"),
                    feels_like_c=current.get("apparent_temperature"),
                    condition="clear" if current.get("temperature_2m", 0) >= 0 else "rain",
                    precipitation_probability=int(current.get("precipitation", 0) or 0),
                )
        except Exception:
            pass

        return WeatherSnapshot(
            temperature_c=18.0,
            feels_like_c=17.0,
            condition="clear",
            precipitation_probability=10,
        )
