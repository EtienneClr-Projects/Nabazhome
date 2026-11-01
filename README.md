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
- `deploy/` : Luckfox source sync, installation, and boot services
- `.agents/skills/luckfox-deploy/` : agent deployment and target debugging workflow

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

## Luckfox Board

The deployment target is a **Luckfox Lyra Zero W**. Its installed Linux image must provide Python 3.11+, uv, rsync, and either systemd or BusyBox init with `/etc/init.d/rcS`. The installer detects the init system; it does not flash or replace the board's OS. On ARM32, uv-managed Python downloads and some binary dependency wheels may be unavailable, so use a compatible board-provided Python and install compiler/development packages if source builds are required.

The current board has been verified as ARMv7 (`armv7l`), Buildroot 2024.02, BusyBox 1.36.1, and Python 3.11.8. uv 0.12.17 is installed at `/root/.local/bin/uv`; SSH key authentication works. This image has no `apt-get`, `curl`, or `ntpd`, and its root filesystem is approximately 193 MB. Keep optional dependencies disabled unless needed.

### Connect

Connect the board to your network and use the configured SSH alias:

```sh
ssh luckfox
```

The current computer's SSH configuration resolves this to `root@luckfox`, port 22. The supplied factory password is `luckfox`; enter it directly at the SSH prompt, never put it in a deployment script. Change the default password with `passwd` on the board. The hostname must resolve on your network; otherwise create an alias in `~/.ssh/config` using the board's IP address:

```sshconfig
Host luckfox
  HostName <board-ip-address>
  User root
```

For repeated deployments, install your existing SSH public key from the computer:

```sh
ssh-copy-id luckfox
```

### Prepare The Board

On the board, check the prerequisites:

```sh
uname -m
cat /etc/os-release
python3 --version
command -v rsync
command -v uv
```

Install Python 3.11+ and rsync using your image's package manager or image build. On Debian/Ubuntu images, `apt-get update && apt-get install -y python3 python3-venv rsync curl ca-certificates` provides the packages, but verify the Python version. Buildroot images need these features included in their firmware and do not necessarily have `apt-get`.

Install uv using its [official installation instructions](https://docs.astral.sh/uv/getting-started/installation/), for example on an internet-connected board:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

The installer finds uv under the SSH user's `~/.local/bin` as well as `PATH`. Dependency installation needs internet access and enough storage for the Python environment. The boot service itself runs the installed Python directly and does not download dependencies at boot.

For this Buildroot image without curl, download the official `uv-armv7-unknown-linux-gnueabihf.tar.gz` release and its `.sha256` file on the computer, verify the checksum, extract it, and copy only the `uv` binary into `/root/.local/bin/uv` on the board. The current binary has already been installed this way.

The board was initially running with a 1970 clock, which prevents HTTPS dependency downloads and makes alarm times incorrect. Check `ssh luckfox date -u` before installing dependencies. To set the board clock from your computer:

```sh
ssh luckfox "date -u -s '@$(date -u +%s)'"
```

This sets the current time only; it does not configure persistent time synchronization. The clock may need correction again after reboot. Configure NTP or RTC support in the board image for reliable unattended alarm scheduling; do not disable TLS certificate verification as a workaround.

### Deploy From Your Computer

From this repository, run:

```sh
sh deploy/deploy.sh
```

An alternative root SSH target can be passed as `sh deploy/deploy.sh root@<board-ip-address>`. The script syncs the complete source tree into `/opt/nabazhome`, installs locked production dependencies, and enables and restarts the boot service. The Calendar extra is installed only when `NABAZHOME_GOOGLE_CALENDAR_ENABLED=true` in `/etc/default/nabazhome`; redeploy after enabling it. uv's download/build cache lives in `/tmp/nabazhome-uv-cache` to conserve persistent flash. The sync excludes Git metadata, local Python environments, caches, databases, and credentials. `rsync --delete` removes stale source files only within `/opt/nabazhome`; excluded target files are preserved.

Runtime configuration is created once at `/etc/default/nabazhome` and preserved on later deployments. The database lives in `/var/lib/nabazhome/nabazhome.db`. Upload Calendar credentials separately when needed, then set `NABAZHOME_GOOGLE_CALENDAR_ENABLED=true` in the configuration and restart:

```sh
scp credentials.json luckfox:/var/lib/nabazhome/credentials.json
ssh luckfox 'chmod 600 /var/lib/nabazhome/credentials.json'
```

Google's first OAuth login may require an interactive session and a reachable callback port; it should not be completed through an unattended boot service.

Open the dashboard at `http://luckfox:8000` (or use the board IP). Keep this unauthenticated dashboard on a trusted network rather than exposing it to the internet.

### Boot And Service Control

The current board uses **BusyBox init**, not systemd. Deployment installs executable `/etc/init.d/S99nabazhome`, which `/etc/init.d/rcS` runs at boot. Use these commands from your computer:

```sh
ssh luckfox '/etc/init.d/S99nabazhome restart'
ssh luckfox '/etc/init.d/S99nabazhome status'
ssh luckfox 'tail -n 100 /var/log/nabazhome.log'
```

To stop or start it explicitly:

```sh
ssh luckfox '/etc/init.d/S99nabazhome stop'
ssh luckfox '/etc/init.d/S99nabazhome start'
```

Deployment syncs `deploy/aliases.sh` and configures `~/.profile` to load it automatically in new SSH login shells, preserving existing profile contents and avoiding duplicate entries. The aliases control the BusyBox service on the current board:

```sh
nabazhome-start
nabazhome-stop
nabazhome-restart
nabazhome-status
```

For an already open shell, run `. /opt/nabazhome/deploy/aliases.sh` once. Aliases belong to the interactive shell; loading them inside the service would not make them available in SSH sessions.

This service starts at boot but does not automatically restart after crashes. `systemctl` and `journalctl` do not work on this image: they require systemd running as PID 1. Installing `systemctl` alone is insufficient; switching init systems requires rebuilding or replacing the board's Linux image. The installer retains systemd support for other images, but it is not used on this board.

The service runs as root to match the board's SSH account and device access. For a manual run, stop the service first, connect with `ssh luckfox`, and run on the board:

```sh
cd /opt/nabazhome
set -a
. /etc/default/nabazhome
set +a
.venv/bin/python main_luckfox.py
```

After stopping the foreground process, run `/etc/init.d/S99nabazhome start` on the board to restore the service.

Service restart and HTTP responses have been verified; an actual reboot has not been tested. To verify boot behavior, reboot the board when it is safe to do so, reconnect, check service status, and request `http://luckfox:8000/api/dashboard`. Also check the clock after reboot. The agent workflow is recorded in `.agents/skills/luckfox-deploy/SKILL.md`.
