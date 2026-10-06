from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    app_name: str = "Nabaztag"
    web_host: str = "0.0.0.0"
    web_port: int = 8000
    debug: bool = False
    db_path: Path = Path("data/nabazhome.db")
    weather_latitude: float = 50.698
    weather_longitude: float = 3.177
    weather_api_key: str = ""

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            app_name=os.getenv("NABAZHOME_APP_NAME", "Nabaztag"),
            web_host=os.getenv("NABAZHOME_HOST", "0.0.0.0"),
            web_port=int(os.getenv("NABAZHOME_PORT", "8000")),
            debug=os.getenv("NABAZHOME_DEBUG", "false").lower() == "true",
            db_path=Path(os.getenv("NABAZHOME_DB_PATH", "data/nabazhome.db")),
            weather_latitude=float(os.getenv("NABAZHOME_LAT", "50.698")),
            weather_longitude=float(os.getenv("NABAZHOME_LON", "3.177")),
            weather_api_key=os.getenv("NABAZHOME_WEATHER_API_KEY", ""),
        )
