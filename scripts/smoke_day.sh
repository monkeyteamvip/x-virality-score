#!/usr/bin/env bash
# Offline sample day for a fresh clone. Does not read config/watchlist.json or call X.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/smoke_day.py
