# Stage 1: Build Tailwind CSS 4 + DaisyUI 5 assets
FROM node:22-slim AS assets
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY static/ ./static/
COPY templates/ ./templates/
COPY apps/ ./apps/
RUN npm run build:css

# Stage 2: Install production Python dependencies with uv
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.6 /uv /uvx /usr/local/bin/
WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Stage 3: Minimal non-root runtime image
FROM python:3.12-slim AS production
WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings.production

COPY --from=builder /app/.venv /app/.venv
COPY manage.py ./
COPY apps/ ./apps/
COPY common/ ./common/
COPY config/ ./config/
COPY templates/ ./templates/
COPY static/ ./static/
COPY --from=assets /app/static/css/dist/output.css ./static/css/dist/output.css

RUN DJANGO_SECRET_KEY=build-only-placeholder-key \
    DJANGO_ALLOWED_HOSTS=localhost \
    DATABASE_URL=sqlite:///tmp/build.sqlite3 \
    python manage.py collectstatic --noinput \
    && rm -f /tmp/build.sqlite3 \
    && addgroup --system django \
    && adduser --system --ingroup django django \
    && chown -R django:django /app

USER django
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["python", "-c", "import urllib.request; req = urllib.request.Request('http://127.0.0.1:8000/health/', headers={'Host': 'localhost'}); urllib.request.urlopen(req, timeout=3)"]

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
