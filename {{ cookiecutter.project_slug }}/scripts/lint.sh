#!/bin/sh

set -e

CURRENT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
BASE_DIR="$(dirname "$CURRENT_DIR")"

pre-commit run --all-files --config "${BASE_DIR}/.pre-commit-config.yaml"
