#!/bin/sh

set -e

CURRENT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
BASE_DIR="$(dirname "$CURRENT_DIR")"

[ -s ".env" ] && \. ".env"

alembic upgrade --tag TEST_RESET head

coverage run --rcfile "${BASE_DIR}/pyproject.toml" --module pytest "${BASE_DIR}/tests" "$*"
coverage html --rcfile "${BASE_DIR}/pyproject.toml"
