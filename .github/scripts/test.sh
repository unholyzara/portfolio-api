#!/usr/bin/env bash

set -euo pipefail

POSTGRES_CONTAINER="portfolio-api-test-postgres"

cleanup() {
  docker rm --force "${POSTGRES_CONTAINER}" >/dev/null 2>&1 || true
}

trap cleanup EXIT

docker run --detach --rm \
  --name "${POSTGRES_CONTAINER}" \
  --env POSTGRES_DB=portfolio_test \
  --env POSTGRES_USER=portfolio \
  --env POSTGRES_PASSWORD=portfolio \
  --publish 5432:5432 \
  postgres:16 >/dev/null

until docker exec "${POSTGRES_CONTAINER}" \
  pg_isready --username portfolio --dbname portfolio_test >/dev/null 2>&1; do
  sleep 1
done

python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r test/requirements.txt

SECRET_KEY=test-secret-key \
DB_NAME=portfolio_test \
DB_USER=portfolio \
DB_PASSWORD=portfolio \
DB_HOST=localhost \
DB_PORT=5432 \
python -m pytest --ds=api.settings test
