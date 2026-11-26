# Django Fullstack Starter Template

🌐 Idioma: [English](./README.md) | **Español**

[![CI](https://github.com/fquivera/django-starter-template/actions/workflows/ci.yml/badge.svg)](https://github.com/fquivera/django-starter-template/actions/workflows/ci.yml)
[![Django 5.2 LTS](https://img.shields.io/badge/Django-5.2%20LTS-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![HTMX 2.0](https://img.shields.io/badge/HTMX-2.0-336699?logo=htmx&logoColor=white)](https://htmx.org/)
[![Tailwind CSS 4](https://img.shields.io/badge/Tailwind%20CSS-4-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![DaisyUI 5](https://img.shields.io/badge/DaisyUI-5-5A0EF8?logo=daisyui&logoColor=white)](https://daisyui.com/)
[![Alpine.js 3](https://img.shields.io/badge/Alpine.js-3-8BC0D0?logo=alpinedotjs&logoColor=white)](https://alpinejs.dev/)
[![uv](https://img.shields.io/badge/uv-Package%20Manager-DE5FE9)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/badge/Code%20Style-Ruff-black)](https://github.com/astral-sh/ruff)

Plantilla base lista para producción para aplicaciones **Django Fullstack** bajo el paradigma **Server-Driven Web Application**: **Django 5.2 LTS** como fuente única de la verdad, **HTMX 2** para actualizaciones parciales de HTML sin complejidad de SPA, **Tailwind CSS 4 + DaisyUI 5** para un sistema de diseño semántico y temático, y **Alpine.js 3** para estado efímero de interfaz.

Diseñada además con una **arquitectura de Skills en 2 capas optimizada para Agentes de IA** (bajo consumo de tokens de entrada por turno, sin perder cobertura técnica).

---

## 📸 Vista Previa

| Tema Claro (`corporate`) | Tema Oscuro (`night`) |
|---|---|
| ![Vista Previa Tema Claro](./docs/images/demo-light.jpeg) | ![Vista Previa Tema Oscuro](./docs/images/demo-dark.jpeg) |

---

## 🎯 Características Principales

- **Gestión Rápida con `uv`**: Resolución reproducible de dependencias y grupos `dev` en [`pyproject.toml`](./pyproject.toml) + `uv.lock`.
- **Settings Divididos por Entorno**: `config/settings/` (`base.py`, `development.py`, `production.py`, `test.py`) administrado con `django-environ`.
- **Custom User Model desde el Día Cero**: `apps.users.User` configurado en `AUTH_USER_MODEL` antes de la primera migración.
- **Tailwind CSS 4 + DaisyUI 5 (*CSS-First*)**: Sin `tailwind.config.js`; temas declarados en [`static/css/input.css`](./static/css/input.css) con cambio dinámico en tiempo real (`corporate`, `emerald`, `winter`, `light`, `dark`, `night`, `synthwave`) persistido en `localStorage`.
- **HTMX 2 + `django-htmx` + Alpine.js 3 Pre-cableados**:
  - Middleware `django_htmx` activo (`request.htmx`) y token CSRF global en `<body>`.
  - Shell de modal dinámico cargado bajo demanda vía HTMX y controlado con Alpine (`ESC`, backdrop, transiciones).
  - Contenedor de notificaciones toast Out-of-Band (`hx-swap-oob`) con auto-cierre.
- **Listo para Docker y Producción**: [`Dockerfile`](./Dockerfile) multi-stage no-root, [`compose.yml`](./compose.yml) (PostgreSQL 16 + perfil opcional `async` con Redis para Huey), WhiteNoise con compresión Brotli y Gunicorn.
- **Quality Gates Automatizados**: `pytest`, `pytest-django`, `ruff` (lint + format) y GitHub Actions CI.
- **AI-Agent Ready de Bajo Consumo**: 6 skills activas en [`.agents/skills/`](./.agents/skills/) + 6 skills especializadas *on-demand* en [`.agents/skills-ondemand/`](./.agents/skills-ondemand/) (~76.7% menos tokens fijos de metadatos por turno frente a catálogos planos).

---

## 📁 Estructura del Proyecto

```text
django-starter-template/
├── .github/                        # CI/CD (GitHub Actions), Dependabot y templates de Issues/PR
├── .agents/
│   ├── skills/                     # 6 Skills activas (Core + Frontend consolidado)
│   │   ├── README.md
│   │   ├── django-architecture/
│   │   ├── django-models-migrations/
│   │   ├── django-views-forms-security/
│   │   ├── django-testing-quality/
│   │   ├── git-workflow/
│   │   └── django-hypermedia-ui/
│   └── skills-ondemand/            # 6 Skills especializadas (0 tokens por defecto)
│       ├── huey-patterns/          # Tareas asíncronas/crons con Huey + Redis
│       ├── django-infrastructure/  # Docker, Gunicorn, Compose, WhiteNoise, CSP
│       ├── django-admin-expert/    # Optimización N+1 y acciones en Django Admin
│       ├── github-actions/         # CI/CD, branch policy, releases
│       ├── i18n/                   # Catálogos .po/.mo y localización
│       └── systematic-debugging/   # Depuración en 4 fases (Root Cause First)
├── apps/
│   ├── core/                       # Landing, demos HTMX y endpoint /health/
│   └── users/                      # Custom User Model & Admin
├── common/                         # Utilidades transversales y helpers compartidos
├── config/                         # Configuración del proyecto (settings/, urls.py, wsgi/asgi)
├── docs/images/                    # Capturas de vista previa del README (temas claro y oscuro)
├── static/
│   ├── css/
│   │   ├── input.css               # Fuente Tailwind CSS 4 + DaisyUI 5 (@plugin)
│   │   └── dist/output.css         # CSS compilado y minificado
│   └── js/
│       ├── htmx.min.js             # HTMX 2 vendorizado
│       └── alpine.min.js           # Alpine.js 3 vendorizado
├── templates/
│   ├── base.html                   # Layout maestro (CSRF, Navbar, Modales y Toasts)
│   ├── components/                 # _navbar.html, _modal_shell.html, _toast_container.html
│   └── pages/                      # home.html y partials/ (_counter_box.html, _modal_demo.html)
├── .dockerignore
├── AGENTES.md                      # Reglas arquitectónicas y Quality Gate para Agentes IA
├── CHANGELOG.md                    # Historial de versiones (Keep a Changelog + SemVer)
├── CONTRIBUTING.md                 # Guía de contribución (GitFlow + Conventional Commits)
├── Dockerfile                      # Imagen multi-stage non-root (Node assets + uv + Gunicorn)
├── README.md                       # Documentación principal (English)
├── README.es.md                    # Documentación en Español
├── SECURITY.md                     # Política de seguridad y reporte responsable
├── compose.yml                     # PostgreSQL 16 + Web + perfil opcional async (Redis)
├── manage.py
├── package.json                    # Tailwind CSS 4 CLI + DaisyUI 5
└── pyproject.toml                  # Dependencias Python, Ruff y pytest
```

---

## 🚀 Inicio Rápido (Quickstart)

### Prerrequisitos

- **Python 3.11+** (recomendado 3.12)
- [**uv**](https://docs.astral.sh/uv/getting-started/installation/) (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Node.js 18+** y **npm**

### Opción A: Desarrollo Local (`uv` + `npm`)

1. En GitHub, haz clic en **"Use this template"** (o clona directamente):
   ```bash
   git clone git@github.com:fquivera/django-starter-template.git mi-proyecto
   cd mi-proyecto
   ```
2. Configura variables de entorno:
   ```bash
   cp .env.example .env
   ```
3. Instala dependencias Python y Node:
   ```bash
   uv sync
   npm install
   npm run build:css
   ```
4. Migra la base de datos y crea un superusuario:
   ```bash
   uv run python manage.py migrate
   uv run python manage.py createsuperuser
   ```
5. Levanta servidor Django y watcher CSS en dos terminales:
   ```bash
   # Terminal 1
   uv run python manage.py runserver

   # Terminal 2
   npm run watch:css
   ```

### Opción B: Levantar con Docker Compose (PostgreSQL + Gunicorn)

```bash
docker compose up --build
```

Para incluir Redis (perfil `async` para Huey cuando habilites tareas en segundo plano):

```bash
docker compose --profile async up --build
```

Accesos locales:
- **Aplicación Web**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Health Check**: [http://127.0.0.1:8000/health/](http://127.0.0.1:8000/health/)

---

## 🏗️ Arquitectura & Decisiones Técnicas

1. **Separación de capas por responsabilidad**:
   - `models.py` / `models/`: invariantes de fila única, `TextChoices` y QuerySets custom (`visible_to()`).
   - `services.py` / `services/`: casos de uso multi-agregado, `@transaction.atomic` e I/O externo.
   - `selectors.py` / `selectors/`: lecturas reutilizables optimizadas con `select_related` / `prefetch_related`.
   - `views.py` / `views/`: traducción HTTP delgada, detección con `request.htmx` y retorno HTTP 200 en errores de formulario HTMX.
2. **Procesamiento asíncrono recomendado con Huey**:
   - Para colas de tareas o tareas periódicas en proyectos pequeños y medianos, este starter adopta **Huey + Redis** (documentado en [`.agents/skills-ondemand/huey-patterns/SKILL.md`](./.agents/skills-ondemand/huey-patterns/SKILL.md)) en lugar de Celery, reduciendo complejidad operativa y consumo de memoria.
3. **Política de Versionado LTS**:
   - La plantilla fija **Django 5.2 LTS** (`django>=5.2.0,<5.3.0` en [`pyproject.toml`](./pyproject.toml)) para garantizar 3 años de estabilidad y actualizaciones de seguridad en producción sin saltos de versión frecuentes. Se mantiene en 5.2 LTS (omitiendo versiones intermedias 6.0/6.1) hasta el lanzamiento de la próxima versión **Django 6.2 LTS**.

---

## 🛠️ Comandos de Desarrollo y Quality Gate

| Tarea | Comando |
|---|---|
| **Ejecutar Suite de Tests** | `uv run pytest` |
| **Linting (Ruff)** | `uv run ruff check .` |
| **Formateo (Ruff)** | `uv run ruff format .` / `uv run ruff format --check .` |
| **Check del Sistema Django** | `uv run python manage.py check` |
| **Verificar Migraciones Limpias** | `uv run python manage.py makemigrations --check --dry-run` |
| **Compilar CSS (Producción)** | `npm run build:css` |
| **Compilar CSS (Desarrollo)** | `npm run watch:css` |

---

## 🧠 Desarrollo Asistido por Agentes de IA

Este repositorio sigue una estructura modular de bajo consumo para asistentes como **Google Antigravity, Claude Code, Cursor o Copilot**:

- [`AGENTES.md`](./AGENTES.md): Contrato principal del proyecto, reglas de seguridad anti-IDOR y Quality Gate obligatorio.
- [`.agents/skills/`](./.agents/skills/): Solo **6 skills activas** (`django-architecture`, `django-models-migrations`, `django-views-forms-security`, `django-testing-quality`, `git-workflow` y `django-hypermedia-ui`), manteniendo el contexto base ligero en cada turno y cargando recetas/componentes desde `references/` únicamente bajo demanda.
- [`.agents/skills-ondemand/`](./.agents/skills-ondemand/): **6 skills bajo demanda** (`huey-patterns`, `django-infrastructure`, `django-admin-expert`, `github-actions`, `i18n`, `systematic-debugging`) que consumen **0 tokens** hasta ser consultadas explícitamente.

---

## 🔀 Flujo de Contribución (GitFlow + Conventional Commits)

Consulta las reglas completas en [`CONTRIBUTING.es.md`](./CONTRIBUTING.es.md) y la política de reporte responsable en [`SECURITY.es.md`](./SECURITY.es.md).

1. Crea una rama desde `develop`:
   ```bash
   git switch develop && git pull --ff-only origin develop
   git switch -c feat/mi-funcionalidad
   ```
2. Realiza commits atómicos siguiendo **Conventional Commits** (`feat(scope): ...`, `fix(scope): ...`, `docs: ...`, `refactor(skills): ...`).
3. Ejecuta el Quality Gate completo (`check`, `makemigrations --check --dry-run`, `pytest`, `ruff check .`, `ruff format --check .`, `npm run build:css`).
4. Abre un Pull Request hacia `develop` con título en formato Conventional Commits (se integrará mediante **Squash Merge**). Las ramas `release/*` y `hotfix/*` se integran a `main` con merge commit (`--no-ff`) y retro-fusión a `develop`.

---

## 🚢 Despliegue en Producción

### Con Docker (Recomendado)

```bash
docker build -t my-django-app:latest .
docker run -d -p 8000:8000 \
  -e DJANGO_SECRET_KEY="<tu-clave-secreta>" \
  -e DJANGO_ALLOWED_HOSTS="tudominio.com" \
  -e CSRF_TRUSTED_ORIGINS="https://tudominio.com" \
  -e DATABASE_URL="postgres://user:pass@host:5432/dbname" \
  my-django-app:latest
```

### Despliegue Manual (Bare Metal / PaaS)

1. Configura las variables de entorno de producción (`DJANGO_SETTINGS_MODULE=config.settings.production`, `DJANGO_DEBUG=False`, `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `DATABASE_URL=postgresql://...`).
2. Instala dependencias de producción sin grupo dev:
   ```bash
   uv sync --frozen --no-dev
   ```
3. Compila el CSS final y recolecta estáticos:
   ```bash
   npm ci && npm run build:css
   uv run python manage.py collectstatic --noinput
   ```
4. Ejecuta las migraciones y levanta el servidor WSGI con Gunicorn (y `huey_consumer.py` si habilitas Huey):
   ```bash
   uv run python manage.py migrate --noinput
   uv run gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
   ```
