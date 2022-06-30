#!/bin/sh

export APP_MODULE=${APP_MODULE-app.main:app}
export HOST=${HOST:-{{ cookiecutter.default_host }}}
export PORT=${PORT:-{{ cookiecutter.default_port }}}

exec uvicorn --reload --host $HOST --port $PORT "$APP_MODULE"
