#!/bin/sh

set -e

CURRENT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
BASE_DIR="$(dirname "$CURRENT_DIR")"

cd $BASE_DIR

docker build --rm --target python-base --tag {{ cookiecutter.project_slug }}-python-base --file docker/Dockerfile .
docker build --rm --target builder-base --tag {{ cookiecutter.project_slug }}-builder-base --file docker/Dockerfile .
docker build --rm --target development --tag {{ cookiecutter.project_slug }}-development --file docker/Dockerfile .
docker build --rm --target production --tag {{ cookiecutter.project_slug }}-production --file docker/Dockerfile .
