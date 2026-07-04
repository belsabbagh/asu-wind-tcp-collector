#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

exec uv run watchfiles "uv run server.py" . --ignore-paths .venv
