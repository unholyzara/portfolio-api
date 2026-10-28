#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Load test environment variables from the project root
set -a
source "${PROJECT_ROOT}/.env.test"
set +a

POSTGRES_CONTAINER="portfolio-api-test-postgres"

cleanup() {
  docker rm --force "${POSTGRES_CONTAINER}" >/dev/null 2>&1 || true
}

trap cleanup EXIT

docker run --detach --rm \
  --name "${POSTGRES_CONTAINER}" \
  --env POSTGRES_DB="${DB_NAME}" \
  --env POSTGRES_USER="${DB_USER}" \
  --env POSTGRES_PASSWORD="${DB_PASSWORD}" \
  --publish "${DB_PORT}:5432" \
  postgres:16 >/dev/null

until docker exec "${POSTGRES_CONTAINER}" \
  pg_isready --username "${DB_USER}" --dbname "${DB_NAME}" >/dev/null 2>&1; do
  sleep 1
done

cd "${PROJECT_ROOT}"

python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r test/requirements.txt

python -m pytest --ds=api.settings test
