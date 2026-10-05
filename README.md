# Nabazhome

This repository contains the active Nabaztag dashboard and device service stack built around a clean layered application structure.

## Current structure

- `nabazhome_luckfox/` : application code
  - `api/` : FastAPI routes and dashboard endpoints
  - `config/` : runtime settings
  - `dashboard/` : HTML/CSS/JS dashboard UI
  - `domain/` : core domain models
  - `drivers/` : hardware abstractions
  - `infrastructure/` : persistence and system glue
  - `repositories/` : data access layer
  - `services/` : orchestration and runtime behavior
- `main.py` : default app entrypoint
- `main_luckfox.py` : compatibility entrypoint for the Luckfox runtime
- `tests/` : project regression tests

## Run locally

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python main.py
```

The app serves the dashboard at the local web root and exposes the live device, alarm, weather, and calendar APIs used by the UI.
