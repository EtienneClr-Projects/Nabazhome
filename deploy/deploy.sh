#!/bin/sh
set -eu

TARGET=${1:-luckfox}
APP_DIR=/opt/nabazhome
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

if [ "$#" -gt 1 ] || ! printf '%s\n' "$TARGET" | LC_ALL=C grep -Eq '^[A-Za-z0-9_][A-Za-z0-9_.@-]*$'; then
    printf 'Usage: sh %s [ssh-host-or-user@host]\n' "$0" >&2
    exit 2
fi
command -v rsync >/dev/null 2>&1 || {
    printf '%s\n' 'Install rsync on your computer first.' >&2
    exit 1
}
ssh "$TARGET" 'test "$(id -u)" -eq 0 && command -v rsync >/dev/null && mkdir -p /opt/nabazhome' || {
    printf '%s\n' 'The SSH target must be root and have rsync installed.' >&2
    exit 1
}

rsync -az --delete --itemize-changes \
    --exclude='.git/' \
    --exclude='.venv/' \
    --exclude='__pycache__/' \
    --exclude='*.py[cod]' \
    --exclude='.pytest_cache/' \
    --exclude='.mypy_cache/' \
    --exclude='.ruff_cache/' \
    --exclude='data/' \
    --exclude='*.db' \
    --exclude='credentials.json' \
    --exclude='token.json' \
    --exclude='.env' \
    --exclude='.env.*' \
    "$ROOT/" "$TARGET:$APP_DIR/"

ssh "$TARGET" 'sh /opt/nabazhome/deploy/install.sh'