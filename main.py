from __future__ import annotations

import uvicorn

from nabazhome_luckfox.api.app import create_app
from nabazhome_luckfox.config.settings import Settings


def main() -> None:
    settings = Settings.from_env()
    app = create_app(settings)
    print(f"{settings.app_name} booting on {settings.web_host}:{settings.web_port}")
    uvicorn.run(app, host=settings.web_host, port=settings.web_port, log_level="info")


if __name__ == "__main__":
    main()
