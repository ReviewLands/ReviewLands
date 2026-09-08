#!/usr/bin/env bash
# Idempotent Cloud Agent setup for the ReviewLands document/PDF toolkit.
# Installs the system libraries WeasyPrint/OpenCV need, Bengali fonts, adb,
# and the pinned Python dependencies.
set -euo pipefail

cd "$(dirname "$0")/.."

SYSTEM_PACKAGES=(
  # WeasyPrint (HTML -> PDF) runtime libraries
  libpango-1.0-0
  libpangocairo-1.0-0
  libpangoft2-1.0-0
  libgdk-pixbuf-2.0-0
  libcairo2
  libffi-dev
  libglib2.0-0
  libjpeg-turbo8
  libharfbuzz0b
  # Bengali script coverage used by the exam/question generators
  fonts-noto-core
  # Android Debug Bridge for the redmi10-adb toolkit
  android-tools-adb
)

echo ">> Installing system packages"
sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends "${SYSTEM_PACKAGES[@]}"

echo ">> Installing Python dependencies"
pip install --break-system-packages --no-cache-dir -r requirements.txt

echo ">> Refreshing font cache"
sudo fc-cache -f >/dev/null 2>&1 || true

echo ">> Setup complete"
