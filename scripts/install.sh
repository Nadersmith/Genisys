#!/usr/bin/env bash
set -e

# Usage: sudo ./install.sh
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root: sudo $0"
  exit 1
fi

PY_VERSION=3
# create venv
python3 -m venv /opt/genisys/venv
/opt/genisys/venv/bin/pip install --upgrade pip
/opt/genisys/venv/bin/pip install -r /opt/genisys/requirements.txt

# create service user
useradd --system --no-create-home genisys || true
mkdir -p /opt/genisys
chown -R genisys:genisys /opt/genisys

echo "Installation complete. Place project files under /opt/genisys and enable systemd unit."
