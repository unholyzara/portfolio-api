#!/bin/bash
set -e

: "${DB_HOST:?DB_HOST is not set}"
: "${DB_PORT:?DB_PORT is not set}"
: "${DB_USER:?DB_USER is not set}"

RETRIES=0
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  RETRIES=$((RETRIES + 1))
  if [ "$RETRIES" -ge 30 ]; then
    echo "Postgres not reachable at ${DB_HOST}:${DB_PORT}" >&2
    exit 1
  fi
  sleep 2
done

python manage.py migrate --noinput

exec "$@"
