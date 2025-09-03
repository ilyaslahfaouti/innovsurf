#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"
BACK_PID_FILE="$BACKEND_DIR/dev_server.pid"
FRONT_PID_FILE="$FRONTEND_DIR/dev_server.pid"

stop_pid() {
  local name="$1"; local file="$2"
  if [ -f "$file" ]; then
    local pid
    pid=$(cat "$file" || true)
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
      echo "Stopping $name (PID $pid)"
      kill "$pid" 2>/dev/null || true
      sleep 1
      if kill -0 "$pid" 2>/dev/null; then
        echo "Force killing $name (PID $pid)"
        kill -9 "$pid" 2>/dev/null || true
      fi
    else
      echo "$name not running"
    fi
    rm -f "$file"
  else
    echo "$name PID file not found ($file)"
  fi
}

stop_pid "backend" "$BACK_PID_FILE"
stop_pid "frontend" "$FRONT_PID_FILE"

echo "Done."


