#!/bin/sh

set -e

CURRENT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
BASE_DIR="$(dirname "$CURRENT_DIR")"

[ -s ".env" ] && \. ".env"

export APP_MODULE=${APP_MODULE-app.main:app}
export HOST=${HOST:-localhost}
export PORT=${PORT:-8001}

exec uvicorn --reload --host $HOST --port $PORT "$APP_MODULE"
