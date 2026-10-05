#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

sudo install -Dm644 \
    "$ROOT/deploy/dailygamebot.service" \
    /etc/systemd/system/dailygamebot.service

cd "$ROOT"
uv sync --locked

sudo systemctl daemon-reload
sudo systemctl restart dailygamebot
