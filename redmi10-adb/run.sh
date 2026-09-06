#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if ! command -v adb >/dev/null 2>&1; then
  echo "adb not found. Install Android platform-tools and add adb to PATH."
  exit 1
fi
if command -v python3 >/dev/null 2>&1; then
  exec python3 redmi10.py "$@"
fi
if command -v python >/dev/null 2>&1; then
  exec python redmi10.py "$@"
fi
echo "Python 3 is required. Install python3 and try again."
exit 1
