# Configuration Rules & Anti-Hardcoding

Deployment values come from environment variables. User choices live in the database. Stable domain facts live in `TextChoices` or `constants.py`.

## Canonical Environment Variables

Keep `.env.example`, `config/settings/base.py`, and this table synchronized:

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `DJANGO_SETTINGS_MODULE` | yes | `config.settings.development` in `manage.py` | Active settings module |
| `DJANGO_SECRET_KEY` | yes (prod) | Dev placeholder only | Django cryptographic signing key |
| `DJANGO_DEBUG` | no | `False` | Debug mode; must be `False` in production |
| `DJANGO_ALLOWED_HOSTS` | prod | `127.0.0.1,localhost` | Comma-separated allowed hostnames |
| `DATABASE_URL` | prod | `sqlite:///db.sqlite3` in dev | PostgreSQL / DB DSN parsed via `env.db()` |
| `CSRF_TRUSTED_ORIGINS` | prod | `http://localhost:8000,http://127.0.0.1:8000` | Comma-separated HTTPS origins |
| `DJANGO_LANGUAGE_CODE` | no | `es-ve` | Default active language code |
| `DJANGO_TIME_ZONE` | no | `America/Caracas` | Default application time zone |
| `EMAIL_BACKEND` | no | `console.EmailBackend` in dev | Email transport backend |
| `REDIS_URL` | optional | `redis://localhost:6379/0` | Cache and Huey task queue broker (when enabled) |
| `HUEY_IMMEDIATE` | optional | `False` (`True` in test) | Run Huey tasks synchronously without a worker |

## Environment Variable Rules

- Read variables exclusively in `config/settings/` using `django-environ` (`env.str`, `env.bool`, `env.int`, `env.list`, `env.db`).
- Never call `os.environ` or `os.getenv` inside `apps/` or `common/`.
- Never ship `.env` in images or commits; keep `.env` git-ignored and `.env.example` complete with non-secret placeholders.
- Production settings (`config/settings/production.py`) must fail fast at startup (`ImproperlyConfigured`) if `DJANGO_SECRET_KEY` is missing/insecure, `DEBUG=True`, or `DJANGO_ALLOWED_HOSTS` is empty.
- Never branch business behavior on `settings.DEBUG` or environment names; use explicit configuration flags or settings.
- Never mutate `django.conf.settings` at runtime; tests must use `@override_settings`.

## Anti-Hardcoding Rules

- **Routes**: use `reverse("app:name")` and `{% url 'app:name' %}` — never literal path strings like `"/users/profile/"` in Python or templates.
- **Settings**: access `django.conf.settings.<KEY>` inside functions/methods rather than copying values into module-level constants at import time.
- **Tunables & limits**: timeouts, page sizes, upload limits, retry counts, and cache TTLs belong in `config/settings/` or `constants.py`, never inline magic numbers in services.
- **External assets**: serve vendor JS/CSS locally under `static/` (supports strict CSP and offline reliability).

## Feature Flags

```python
FEATURE_NEW_DASHBOARD = env.bool("DJANGO_FEATURE_NEW_DASHBOARD", default=False)
```

- Default flags to `False`, test both states when active, and delete the flag plus dead branch once rollout completes.

## Anti-Patterns

- Scattered `os.getenv()` calls in views, forms, or services.
- Secondary YAML/JSON config files duplicating environment variables.
- Secrets with production defaults.
- Hardcoded URLs, hosts, ports, email addresses, or hex colors in `apps/` or `templates/`.
