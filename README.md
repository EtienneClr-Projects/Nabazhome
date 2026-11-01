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

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) first. The project requires Python 3.11 or newer; uv can install Python automatically if needed.

```bash
uv sync --locked
uv run main.py
```

uv manages the local `.venv` automatically, so manual creation and activation are not needed. Dependencies are declared in `pyproject.toml` and pinned in `uv.lock`.

For Google Calendar support, install the optional dependencies and run with the same extra:

```bash
uv sync --locked --extra calendar
uv run --extra calendar main.py
```

The Luckfox compatibility entrypoint can be run with `uv run main_luckfox.py`.

The app serves the dashboard at the local web root and exposes the live device, alarm, weather, and calendar APIs used by the UI.

## Run tests

```bash
uv run python -m unittest discover -s tests -p 'test_*.py'
```

## Manage dependencies

Use `uv add <package>` for runtime dependencies or `uv add --dev <package>` for development dependencies. Commit both `pyproject.toml` and `uv.lock` when dependencies change.
