# portfolio-django-template

Base template for Django microservices in the portfolio project.

## Structure

```
├── core/
│   ├── settings.py         # All config from environment variables
│   ├── urls.py             # Root URLs, delegates to service/urls.py
│   ├── wsgi.py
│   └── __init__.py
├── service/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py            # Includes /api/health/ endpoint
│   ├── urls.py
│   ├── apps.py
│   └── __init__.py
├── manage.py
├── requirements.txt
├── entrypoint.sh           # Waits for postgres, then starts gunicorn
├── Dockerfile
└── .env.example
```

## Local development

```bash
cp .env.example .env
docker compose up --build
```

The health endpoint is available at `http://localhost:8000/api/health/`.

## Environment variables

All configuration comes from environment variables — no hardcoded values.
In local they are read from `.env`. In beta and prd they are injected by
the deploy pipeline from SSM Parameter Store before the container starts.

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `true` or `false` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts |
| `DB_HOST` | Postgres host |
| `DB_PORT` | Postgres port |
| `DB_NAME` | Database name |
| `DB_USER` | Database user |
| `DB_PASSWORD` | Database password |
| `LOG_LEVEL` | Logging level (`DEBUG`, `INFO`, `WARNING`) |
