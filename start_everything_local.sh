#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"
BACK_PID_FILE="$BACKEND_DIR/dev_server.pid"
FRONT_PID_FILE="$FRONTEND_DIR/dev_server.pid"

echo "Starting InnovSurf (backend + frontend)"

if [ -f "$BACK_PID_FILE" ] && kill -0 "$(cat "$BACK_PID_FILE")" 2>/dev/null; then
  echo "Backend already running with PID $(cat "$BACK_PID_FILE")"
else
  echo "Launching backend..."
  cd "$BACKEND_DIR"
  if [ -x ./venv310/bin/python ]; then PY=./venv310/bin/python; else PY=python3; fi
  $PY -m pip install -r requirements.txt
  $PY manage.py migrate
  nohup $PY manage.py runserver 0.0.0.0:8000 > "$BACKEND_DIR/server.log" 2>&1 & echo $! > "$BACK_PID_FILE"
  echo "Backend started on http://localhost:8000 (PID $(cat "$BACK_PID_FILE"))"
fi

if [ -f "$FRONT_PID_FILE" ] && kill -0 "$(cat "$FRONT_PID_FILE")" 2>/dev/null; then
  echo "Frontend already running with PID $(cat "$FRONT_PID_FILE")"
else
  echo "Launching frontend..."
  cd "$FRONTEND_DIR"
  npm install --no-fund --no-audit
  nohup npm start > "$FRONTEND_DIR/frontend_dev.log" 2>&1 & echo $! > "$FRONT_PID_FILE"
  echo "Frontend started on http://localhost:3000 (PID $(cat "$FRONT_PID_FILE"))"
fi

echo "Done."


