#!/bin/sh
set -eu

if [ "$(id -u)" -ne 0 ]; then
    printf '%s\n' 'Run this installer as root on the Luckfox.' >&2
    exit 1
fi

APP_DIR=/opt/nabazhome
export PATH="$HOME/.local/bin:$PATH"
command -v uv >/dev/null 2>&1 || {
    printf '%s\n' 'Install uv on the board first; see README.md.' >&2
    exit 1
}
command -v python3 >/dev/null 2>&1 || {
    printf '%s\n' 'Install Python 3.11 or newer on the board first.' >&2
    exit 1
}
python3 -c 'import sys; sys.exit(sys.version_info < (3, 11))' || {
    printf '%s\n' 'The board needs Python 3.11 or newer.' >&2
    exit 1
}

if command -v systemctl >/dev/null 2>&1 && [ -d /run/systemd/system ]; then
    INIT=systemd
elif [ -f /etc/init.d/rcS ] && command -v start-stop-daemon >/dev/null 2>&1; then
    INIT=busybox
else
    printf '%s\n' 'Unsupported init system: use systemd or BusyBox with /etc/init.d/rcS.' >&2
    exit 1
fi

cd "$APP_DIR"
mkdir -p /etc/default /var/lib/nabazhome
chmod 700 /var/lib/nabazhome
if [ ! -f /etc/default/nabazhome ]; then
    cp deploy/nabazhome.env.example /etc/default/nabazhome
    chmod 600 /etc/default/nabazhome
fi
set -a
. /etc/default/nabazhome
set +a
set -- --locked --no-dev --python "$(command -v python3)"
if [ "${NABAZHOME_GOOGLE_CALENDAR_ENABLED:-false}" = true ]; then
    set -- "$@" --extra calendar
fi
UV_PYTHON_DOWNLOADS=never UV_CACHE_DIR=/tmp/nabazhome-uv-cache uv sync "$@"

if [ "$INIT" = systemd ]; then
    cp deploy/nabazhome.service /etc/systemd/system/nabazhome.service
    chmod 644 /etc/systemd/system/nabazhome.service
    systemctl daemon-reload
    systemctl enable nabazhome.service
    systemctl restart nabazhome.service
    systemctl --no-pager --full status nabazhome.service
else
    cp deploy/S99nabazhome /etc/init.d/S99nabazhome
    chmod 755 /etc/init.d/S99nabazhome
    /etc/init.d/S99nabazhome restart
    /etc/init.d/S99nabazhome status
fi