#!/bin/sh

[ -s ".env" ] && \. ".env"

export APP_MODULE=${APP_MODULE-app.main:app}
export HOST=${HOST:-{{ cookiecutter.default_local_host }}}
export PORT=${PORT:-{{ cookiecutter.default_local_port }}}

exec uvicorn --reload --host $HOST --port $PORT "$APP_MODULE"
