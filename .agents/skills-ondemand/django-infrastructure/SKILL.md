---
name: django-infrastructure
description: >
  Production deployment infrastructure for Django: Docker multi-stage builds, Gunicorn, Compose, WhiteNoise, Tailwind 4 CSS build, and CSP headers.
  Use when configuring containers, production settings, static assets, or security headers.
---

# Django Production Infrastructure

Reference for packaging and deploying a server-driven Django + HTMX + Tailwind 4 + DaisyUI 5 application.

> Layering (`models`/`services`/`selectors`/`views`), modular packages, and env rules live in `.agents/skills/django-architecture/`.

## 1. Environment Dependencies (`pyproject.toml` + `uv`)

Keep dev tools (`pytest`, `ruff`) strictly in `[dependency-groups].dev` in `pyproject.toml`. Production images install runtime dependencies only:

```bash
uv sync --frozen --no-dev
```

## 2. Static Assets & Tailwind 4 + DaisyUI 5 Build

- Compile CSS with `npm run build:css` (`tailwindcss -i ./static/css/input.css -o ./static/css/dist/output.css --minify`) before `collectstatic`.
- Commit `static/css/dist/output.css` (or build in the asset stage of `Dockerfile`) so production has zero Node runtime dependency.
- Serve static files with **WhiteNoise** (`CompressedManifestStaticFilesStorage` in `config/settings/production.py`).
- Serve vendor scripts (`htmx.min.js`, `alpine.min.js`) from `static/js/` so strict CSP requires no third-party CDNs.

## 3. Multi-Stage `Dockerfile` (Non-Root + `uv` + Gunicorn)

```dockerfile
FROM node:22-slim AS assets
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY static/ ./static/
COPY templates/ ./templates/
COPY apps/ ./apps/
RUN npm run build:css

FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

FROM python:3.12-slim AS production
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings.production

COPY --from=builder /app/.venv /app/.venv
COPY . .
COPY --from=assets /app/static/css/dist/output.css ./static/css/dist/output.css

RUN addgroup --system django && adduser --system --ingroup django django \
    && chown -R django:django /app
USER django

RUN DJANGO_SECRET_KEY=build-only python manage.py collectstatic --noinput
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

Never run `manage.py runserver` in production.

## 4. Docker Compose & Optional Huey Worker

- Pin service versions (`postgres:16-alpine`, `redis:7-alpine`) and define `healthcheck` directives so `web` and `worker` wait for database/Redis readiness.
- If async jobs are enabled (see `huey-patterns`), run a dedicated `worker` service executing `huey_consumer.py config.huey.huey` from the same production image.

## 5. Security Headers & CSP

- Run `uv run python manage.py check --deploy` against `config.settings.production` in CI.
- Enforce `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_HSTS_SECONDS`, `X_FRAME_OPTIONS = "DENY"`, and `SECURE_CONTENT_TYPE_NOSNIFF = True`.
- When adding `django-csp`, place `CSPMiddleware` directly after `SecurityMiddleware` with `default-src 'self'`, `script-src 'self'`, `style-src 'self'`, `object-src 'none'`, `frame-ancestors 'none'`, and keep HTMX indicator styles in `static/css/input.css` (`includeIndicatorStyles=false`).

## Integration with Other Skills

- `django-architecture`: Split settings (`config/settings/`) and env validation.
- `.agents/skills-ondemand/huey-patterns/SKILL.md`: Redis + Huey consumer deployment.
- `.agents/skills-ondemand/github-actions/SKILL.md`: CI checks and container publishing.
