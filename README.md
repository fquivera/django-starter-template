# Django Fullstack Starter Template

🌐 Language: **English** | [Español](./README.es.md)

[![CI](https://github.com/fquivera/django-starter-template/actions/workflows/ci.yml/badge.svg)](https://github.com/fquivera/django-starter-template/actions/workflows/ci.yml)
[![Django 5.2 LTS](https://img.shields.io/badge/Django-5.2%20LTS-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![HTMX 2.0](https://img.shields.io/badge/HTMX-2.0-336699?logo=htmx&logoColor=white)](https://htmx.org/)
[![Tailwind CSS 4](https://img.shields.io/badge/Tailwind%20CSS-4-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![DaisyUI 5](https://img.shields.io/badge/DaisyUI-5-5A0EF8?logo=daisyui&logoColor=white)](https://daisyui.com/)
[![Alpine.js 3](https://img.shields.io/badge/Alpine.js-3-8BC0D0?logo=alpinedotjs&logoColor=white)](https://alpinejs.dev/)
[![uv](https://img.shields.io/badge/uv-Package%20Manager-DE5FE9)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/badge/Code%20Style-Ruff-black)](https://github.com/astral-sh/ruff)

Production-ready starter template for modern **Django Fullstack** applications built around the **Server-Driven Web Application** paradigm: **Django 5.2 LTS** as the single source of truth, **HTMX 2** for reactive HTML fragment swaps without SPA overhead, **Tailwind CSS 4 + DaisyUI 5** for a semantic themed design system, and **Alpine.js 3** for transient client-side state.

Includes a **low-token 2-layer AI Agent skills architecture** designed to minimize per-turn context consumption without sacrificing engineering rigor.

---

## 📸 Preview

| Light Theme (`corporate`) | Dark Theme (`night`) |
|---|---|
| ![Light Theme Preview](./docs/images/demo-light.jpeg) | ![Dark Theme Preview](./docs/images/demo-dark.jpeg) |

---

## 🎯 Key Features

- **Fast Dependency Management with `uv`**: Reproducible resolution and separated `dev` dependency groups in [`pyproject.toml`](./pyproject.toml) + `uv.lock`.
- **Environment-Split Settings**: `config/settings/` (`base.py`, `development.py`, `production.py`, `test.py`) wired with `django-environ`.
- **Custom User Model from Day One**: `apps.users.User` configured via `AUTH_USER_MODEL` prior to the initial migration.
- **Tailwind CSS 4 + DaisyUI 5 (*CSS-First*)**: Zero `tailwind.config.js`; themes declared in [`static/css/input.css`](./static/css/input.css) with live theme switching (`corporate`, `emerald`, `winter`, `light`, `dark`, `night`, `synthwave`) persisted in `localStorage`.
- **Pre-Wired HTMX 2 + `django-htmx` + Alpine.js 3**:
  - `django_htmx` middleware active (`request.htmx`) and global CSRF `hx-headers` on `<body>`.
  - On-demand server-rendered modal shell controlled with Alpine (`ESC`, backdrop, transitions).
  - Out-of-Band (`hx-swap-oob`) toast notification container with auto-dismiss.
- **Docker & Production Ready**: Multi-stage non-root [`Dockerfile`](./Dockerfile), [`compose.yml`](./compose.yml) (PostgreSQL 16 + optional `async` profile with Redis for Huey), WhiteNoise Brotli static compression, and Gunicorn.
- **Automated Quality Gates**: `pytest`, `pytest-django`, `ruff` (lint + format), and GitHub Actions CI.
- **Low-Token AI-Agent Ready**: 6 active skills in [`.agents/skills/`](./.agents/skills/) + 6 on-demand skills in [`.agents/skills-ondemand/`](./.agents/skills-ondemand/) (~76.7% fewer fixed metadata tokens per turn compared to flat skill catalogs).

---

## 📁 Project Structure

```text
django-starter-template/
├── .github/                        # GitHub Actions CI, Dependabot, Issue & PR templates
├── .agents/
│   ├── skills/                     # 6 active skills (Core + consolidated Frontend)
│   │   ├── README.md
│   │   ├── django-architecture/
│   │   ├── django-models-migrations/
│   │   ├── django-views-forms-security/
│   │   ├── django-testing-quality/
│   │   ├── git-workflow/
│   │   └── django-hypermedia-ui/
│   └── skills-ondemand/            # 6 specialized skills (0 tokens loaded by default)
│       ├── huey-patterns/          # Async & scheduled jobs with Huey + Redis
│       ├── django-infrastructure/  # Docker, Gunicorn, Compose, WhiteNoise, CSP
│       ├── django-admin-expert/    # N+1-free Django Admin & atomic bulk actions
│       ├── github-actions/         # CI/CD, branch policy, releases
│       ├── i18n/                   # Translation catalogs (.po/.mo) & localization
│       └── systematic-debugging/   # Four-phase root-cause debugging
├── apps/
│   ├── core/                       # Landing page, HTMX demos, and /health/ endpoint
│   └── users/                      # Custom User model & Admin
├── common/                         # Shared helpers and cross-app utilities
├── config/                         # Project configuration (settings/, urls.py, wsgi/asgi)
├── docs/images/                    # README preview screenshots (light & dark themes)
├── static/
│   ├── css/
│   │   ├── input.css               # Tailwind CSS 4 + DaisyUI 5 source (@plugin)
│   │   └── dist/output.css         # Compiled & minified stylesheet
│   └── js/
│       ├── htmx.min.js             # Vendored HTMX 2
│       └── alpine.min.js           # Vendored Alpine.js 3
├── templates/
│   ├── base.html                   # Master layout (CSRF, Navbar, Modal Shell, Toasts)
│   ├── components/                 # _navbar.html, _modal_shell.html, _toast_container.html
│   └── pages/                      # home.html and partials/ (_counter_box.html, _modal_demo.html)
├── .dockerignore
├── AGENTES.md                      # AI Agent architectural rules & Quality Gate
├── CHANGELOG.md                    # Version history (Keep a Changelog + SemVer)
├── CONTRIBUTING.md                 # Contribution guide (GitFlow + Conventional Commits)
├── Dockerfile                      # Multi-stage non-root image (Node assets + uv + Gunicorn)
├── README.md                       # Primary documentation (English)
├── README.es.md                    # Spanish documentation
├── SECURITY.md                     # Security policy & responsible disclosure
├── compose.yml                     # PostgreSQL 16 + Web + optional async profile (Redis)
├── manage.py
├── package.json                    # Tailwind CSS 4 CLI + DaisyUI 5
└── pyproject.toml                  # Python dependencies, Ruff, and pytest config
```

---

## 🚀 Quickstart

### Prerequisites

- **Python 3.11+** (3.12 recommended)
- [**uv**](https://docs.astral.sh/uv/getting-started/installation/) (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Node.js 18+** and **npm**

### Option A: Local Development (`uv` + `npm`)

1. Click **"Use this template"** on GitHub (or clone directly):
   ```bash
   git clone git@github.com:fquivera/django-starter-template.git my-project
   cd my-project
   ```
2. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
3. Install Python and Node dependencies:
   ```bash
   uv sync
   npm install
   npm run build:css
   ```
4. Apply migrations and create a superuser:
   ```bash
   uv run python manage.py migrate
   uv run python manage.py createsuperuser
   ```
5. Start Django and the CSS watcher in two terminals:
   ```bash
   # Terminal 1
   uv run python manage.py runserver

   # Terminal 2
   npm run watch:css
   ```

### Option B: Docker Compose (PostgreSQL + Gunicorn)

```bash
docker compose up --build
```

Include Redis (`async` profile for Huey background tasks when enabled):

```bash
docker compose --profile async up --build
```

Local URLs:
- **Web App**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Health Check**: [http://127.0.0.1:8000/health/](http://127.0.0.1:8000/health/)

---

## 🏗️ Architecture & Technical Decisions

1. **Layered Responsibility Boundaries**:
   - `models.py` / `models/`: single-row invariants, `TextChoices`, and custom QuerySets (`visible_to()`).
   - `services.py` / `services/`: multi-aggregate workflows, `@transaction.atomic`, and external I/O.
   - `selectors.py` / `selectors/`: reusable read-only queries with `select_related` / `prefetch_related`.
   - `views.py` / `views/`: thin HTTP translation, `request.htmx` detection, and HTTP 200 re-renders on invalid HTMX forms.
2. **Huey + Redis over Celery**:
   - For background queues and periodic jobs in small-to-medium projects, this starter standardizes on **Huey + Redis** (documented in [`.agents/skills-ondemand/huey-patterns/SKILL.md`](./.agents/skills-ondemand/huey-patterns/SKILL.md)) for minimal configuration and low memory overhead.
3. **Django 5.2 LTS Versioning Policy**:
   - Pinned to **Django 5.2 LTS** (`django>=5.2.0,<5.3.0` in [`pyproject.toml`](./pyproject.toml)) to provide 3 years of production stability and security updates, skipping intermediate non-LTS releases (`6.0`/`6.1`) until **Django 6.2 LTS** is released.

---

## 🛠️ Development & Quality Gate Commands

| Task | Command |
|---|---|
| **Run Test Suite** | `uv run pytest` |
| **Linting (Ruff)** | `uv run ruff check .` |
| **Formatting (Ruff)** | `uv run ruff format .` / `uv run ruff format --check .` |
| **Django System Check** | `uv run python manage.py check` |
| **Check Clean Migrations** | `uv run python manage.py makemigrations --check --dry-run` |
| **Build CSS (Production)** | `npm run build:css` |
| **Watch CSS (Development)** | `npm run watch:css` |

---

## 🧠 AI-Assisted Development

This repository uses a token-efficient skill structure compatible with **Google Antigravity, Claude Code, Cursor, and Copilot**:

- [`AGENTES.md`](./AGENTES.md): Core architectural contract, anti-IDOR rules, and mandatory Quality Gate.
- [`.agents/skills/`](./.agents/skills/): Only **6 active skills** (`django-architecture`, `django-models-migrations`, `django-views-forms-security`, `django-testing-quality`, `git-workflow`, and `django-hypermedia-ui`), keeping fixed prompt overhead minimal while loading recipes and component guides from `references/` on demand.
- [`.agents/skills-ondemand/`](./.agents/skills-ondemand/): **6 on-demand skills** (`huey-patterns`, `django-infrastructure`, `django-admin-expert`, `github-actions`, `i18n`, `systematic-debugging`) costing **0 tokens** unless explicitly read.

---

## 🔀 Contributing (GitFlow + Conventional Commits)

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for full guidelines and [`SECURITY.md`](./SECURITY.md) for responsible vulnerability disclosure.

1. Branch from `develop`:
   ```bash
   git switch develop && git pull --ff-only origin develop
   git switch -c feat/my-feature
   ```
2. Make atomic commits following **Conventional Commits** (`feat(scope): ...`, `fix(scope): ...`, `docs: ...`, `refactor(skills): ...`).
3. Run the full Quality Gate (`check`, `makemigrations --check --dry-run`, `pytest`, `ruff check .`, `ruff format --check .`, `npm run build:css`).
4. Open a Pull Request targeting `develop` with a Conventional Commit title (**Squash Merge**). `release/*` and `hotfix/*` branches merge into `main` via `--no-ff` merge commits and back-merge into `develop`.

---

## 🚢 Production Deployment

### With Docker (Recommended)

```bash
docker build -t my-django-app:latest .
docker run -d -p 8000:8000 \
  -e DJANGO_SECRET_KEY="<your-secret-key>" \
  -e DJANGO_ALLOWED_HOSTS="yourdomain.com" \
  -e CSRF_TRUSTED_ORIGINS="https://yourdomain.com" \
  -e DATABASE_URL="postgres://user:pass@host:5432/dbname" \
  my-django-app:latest
```

### Manual Deployment (Bare Metal / PaaS)

1. Set production environment variables (`DJANGO_SETTINGS_MODULE=config.settings.production`, `DJANGO_DEBUG=False`, `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `DATABASE_URL=postgresql://...`).
2. Install runtime dependencies only:
   ```bash
   uv sync --frozen --no-dev
   ```
3. Compile CSS and collect static assets:
   ```bash
   npm ci && npm run build:css
   uv run python manage.py collectstatic --noinput
   ```
4. Apply migrations and start Gunicorn (plus `huey_consumer.py` if Huey is enabled):
   ```bash
   uv run python manage.py migrate --noinput
   uv run gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
   ```
