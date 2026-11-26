# Contributing Guide (`CONTRIBUTING.md`)

🌐 Language: **English** | [Español](./CONTRIBUTING.es.md)

Thank you for your interest in contributing to **Django Fullstack Starter Template**!

This template is designed to stay clean, generic, and production-ready on **Django 5.2 LTS + HTMX 2 + Alpine.js 3 + Tailwind CSS 4 + DaisyUI 5**.

---

## 1. Local Environment Setup

### Option A: Local (`uv` + `npm`)

```bash
git clone git@github.com:fquivera/django-starter-template.git
cd django-starter-template
cp .env.example .env
uv sync
npm install
npm run build:css
uv run python manage.py migrate
```

### Option B: Docker Compose

```bash
docker compose up --build
```

---

## 2. GitFlow & Conventional Commits

1. **Working branches:**
   - Always branch from `develop`:
     ```bash
     git switch develop && git pull --ff-only origin develop
     git switch -c feat/my-improvement
     ```
   - Recommended prefixes: `feat/*`, `fix/*`, `docs/*`, `refactor/*`, `test/*`, `ci/*`, `chore/*`.
   - `release/*` and `hotfix/*` branches are cut from `main`, merged via merge commit (`--no-ff`), and back-merged into `develop`.

2. **Commit & PR Title Format (Conventional Commits):**
   ```text
   <type>(<scope>)!: <imperative lowercase description without trailing period>
   ```
   - Valid types: `feat`, `fix`, `perf`, `refactor`, `docs`, `test`, `build`, `ci`, `style`, `chore`, `revert`.
   - Suggested scopes: `core`, `users`, `ui`, `common`, `config`, `deps`, `ci`, `infra`, `skills`, `docs`, `release`.

---

## 3. Mandatory Quality Gate

Before opening a Pull Request targeting `develop`, verify every check passes locally:

```bash
npm run build:css
git diff --exit-code -- static/css/dist/output.css
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

---

## 4. Template & AI Skill Principles

- **Keep the starter generic:** avoid domain-specific business logic or naming from any single application.
- **LTS policy:** we pin **Django 5.2 LTS** (`>=5.2.0,<5.3.0`) until **Django 6.2 LTS** is released.
- **Recommended async queue:** prefer **Huey + Redis** over Celery.
- When using AI assistants or editing `.agents/`, follow [`AGENTES.md`](./AGENTES.md) and [`.agents/skills/README.md`](./.agents/skills/README.md).
