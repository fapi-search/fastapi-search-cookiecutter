#!/bin/sh

alembic upgrade --tag TEST_RESET head
pytest --cov=app tests/
