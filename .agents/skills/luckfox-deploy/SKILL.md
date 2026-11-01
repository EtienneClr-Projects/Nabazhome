---
name: luckfox-deploy
description: "Use when deploying Nabazhome to the Luckfox Lyra Zero W, rerunning code on the target, restarting its boot service, or inspecting target logs."
---

# Luckfox Deployment

The target is the Luckfox Lyra Zero W reached through the local SSH alias `luckfox`. Deployment requires root access. Code lives in `/opt/nabazhome`; persistent data and OAuth files live in `/var/lib/nabazhome`. See `README.md` for initial board setup.

Verified target: ARMv7 (`armv7l`), Buildroot 2024.02, BusyBox 1.36.1, Python 3.11.8, and uv 0.12.17 at `/root/.local/bin/uv`. Passwordless SSH works. Use the BusyBox commands below on this image; it has no systemd, apt-get, curl, or ntpd. The root filesystem is only about 193 MB.

## Deploy Changed Code

1. Inspect `git status --short` and run the relevant local tests.
2. From the repository root run `sh deploy/deploy.sh`. This rsyncs source and the uv lockfile, preserves excluded target environments and data, installs locked production dependencies, and enables/restarts the boot service.
3. Check the target service and dashboard response using the commands below. Do not report deployment or boot verification as successful without target evidence.

The Calendar extra is installed only when `/etc/default/nabazhome` enables `NABAZHOME_GOOGLE_CALENDAR_ENABLED=true`. Redeploy after enabling it. uv caches downloads/builds in `/tmp/nabazhome-uv-cache`, not persistent flash.

Before downloading dependencies, check `ssh luckfox date -u`. The board originally booted with a 1970 clock; invalid time causes TLS certificate failures and incorrect alarm scheduling. When needed, set its clock from the computer using `ssh luckfox "date -u -s '@$(date -u +%s)'"`. This is not persistent NTP configuration. Never disable certificate verification. Reboot timekeeping remains unverified.

The script uses `rsync --delete` only inside `/opt/nabazhome`; do not change its destination or remove exclusions for credentials, data, and `.venv`. It does not upload secrets. Do not commit, push, reboot the board, or change its OS unless the user asks.

## Restart And Inspect

Use BusyBox init on the current board. Do not use `systemctl` or `journalctl`: systemd is not running as PID 1, and installing its client alone will not change that.

```sh
ssh luckfox '/etc/init.d/S99nabazhome restart'
ssh luckfox '/etc/init.d/S99nabazhome status; test -x /etc/init.d/S99nabazhome'
ssh luckfox 'tail -n 100 /var/log/nabazhome.log'
```

Deployment installs executable `/etc/init.d/S99nabazhome`, which `/etc/init.d/rcS` runs at boot. The service does not automatically restart after crashes. An installed boot script is not evidence of a successful reboot test.

Check HTTP from the computer with `curl --fail http://luckfox:8000/api/dashboard` (adjust the configured port if needed).

## Foreground Debugging

Stop the service from the computer to avoid binding the same port twice, then connect:

```sh
ssh luckfox '/etc/init.d/S99nabazhome stop'
ssh luckfox
```

On the target, run:

```sh
cd /opt/nabazhome
set -a
. /etc/default/nabazhome
set +a
.venv/bin/python main_luckfox.py
```

After stopping the foreground process, run `/etc/init.d/S99nabazhome start` on the target, or `ssh luckfox '/etc/init.d/S99nabazhome start'` from the computer.

## Safety And Prerequisites

- Never embed or echo SSH passwords, OAuth credentials, or tokens. If SSH asks for a password, have the user enter it directly in the terminal; do not request it through agent questions or send it through tools.
- Prefer existing SSH keys. If authentication fails, report the blocker rather than working around it with password automation.
- The installer detects systemd or BusyBox init and needs target `uv`, Python 3.11+, and rsync. ARM32 may require a compatible OS/toolchain and source builds; do not assume uv can download Python for it.
- Keep `/etc/default/nabazhome` and `/var/lib/nabazhome` intact across deployments. Configuration changes require restarting the service.