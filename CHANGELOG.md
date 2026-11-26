# Changelog

Todos los cambios notables de este proyecto se documentarán en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/), y este proyecto se adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [0.3.2] - 2026-11-26

### Added
- Agregadas capturas de vista previa en temas claro (`corporate`) y oscuro (`night`) en `docs/images/demo-light.jpeg` y `docs/images/demo-dark.jpeg`.
- Añadidas secciones de vista previa lado a lado y estructura actualizada en `README.md` y `README.es.md`.

### Changed
- Excluido `docs` en `.dockerignore` para mantener mínimo el contexto de compilación Docker.

## [0.3.1] - 2026-11-26

### Fixed
- Migrado `templates/components/_modal_shell.html` a `<dialog class="modal">` nativo de DaisyUI 5 con `<form method="dialog" class="modal-backdrop">` y restauración limpia vía `<template x-ref="loadingTemplate">`, corrigiendo el cierre visual inmediato tras la transición de Alpine.
- Alineado el selector de temas en `templates/components/_navbar.html` con `dropdown-open` / `dropdown-close` de DaisyUI 5.
- Agregado `source(none)` en `static/css/input.css` para compilaciones CSS 100% deterministas (reduciendo `static/css/dist/output.css` de 359 KB a 95 KB y eliminando falsos positivos de escaneo).
- Agregados tests de regresión del modal en `apps/core/tests.py`.

### Security & Dependencies
- Actualizado `django` de `5.2.18` a `5.2.19` (parche de seguridad CVE de Django 5.2 LTS), `gunicorn` `26.2.0 → 27.0.1`, `ruff` `0.17.3 → 0.17.6` y GitHub Actions (`checkout`, `setup-uv`, `setup-node` a `v7`).

## [0.3.0] - 2026-11-26

### Added
- **CI/CD y Salud Comunitaria (`.github/`):**
  - Workflow de GitHub Actions (`.github/workflows/ci.yml`) con jobs `Lint & Assets` (Ruff lint/format, build Tailwind 4 + verificación de drift CSS y validación de `docker compose config`), `Django Checks` (`check`, `makemigrations --check --dry-run` y `check --deploy --fail-level WARNING`) y `Test` en matriz Python `3.12` / `3.13`.
  - `.github/dependabot.yml` con actualizaciones semanales agrupadas para `uv`, `npm` y `github-actions` apuntando a `develop`.
  - Formularios de Issues (`bug_report.yml`, `feature_request.yml`, `config.yml` enlazando Discussions) y `.github/pull_request_template.md`.
- **Docker listo para producción:** `Dockerfile` multi-stage non-root (`node:22-slim` → `python:3.12-slim` + `uv` → runtime Gunicorn con `collectstatic` y `HEALTHCHECK` en `/health/`), `.dockerignore` y `compose.yml` (PostgreSQL 16 + perfil opcional `async` con Redis para Huey).
- **Documentación bilingüe completa:** `README.md` / `README.es.md`, `CONTRIBUTING.md` / `CONTRIBUTING.es.md` y `SECURITY.md` / `SECURITY.es.md` con selector de idioma superior (inglés por defecto + español).

### Changed
- `DJANGO_LANGUAGE_CODE` y `DJANGO_TIME_ZONE` configurables vía variables de entorno con `django-environ` en `config/settings/base.py`, `.env.example` y `configuration-rules.md`.
- `SESSION_COOKIE_SECURE` y `CSRF_COOKIE_SECURE` configurables por entorno (por defecto `True`) en `config/settings/production.py` para permitir pruebas locales HTTP en Docker Compose sin debilitar producción.
- Organización de prueba en `apps/users/tests.py` actualizada al valor genérico `"Acme Corp"`.

## [0.2.0] - 2026-11-26

### Added
- **Arquitectura de Skills en 2 capas de bajo consumo:** 6 skills activas en `.agents/skills/` (5 Core + 1 Frontend consolidada) y 6 skills especializadas *on-demand* en `.agents/skills-ondemand/` (0 tokens cargados por defecto), reduciendo en ~76.7% los tokens fijos de metadatos por turno.
- **Skill `huey-patterns` on-demand:** Guía completa de tareas asíncronas y periódicas con **Huey + Redis** como estándar recomendado sobre Celery por su simplicidad y bajo consumo de recursos.
- **Política de versionado Django 5.2 LTS:** Documentación explícita en `README.md`, `AGENTES.md`, `django-architecture` y plantillas UI para mantener la rama LTS de 3 años hasta el lanzamiento de **Django 6.2 LTS**.
- Flujo **GitFlow** con rama permanente `develop` y archivo `CHANGELOG.md`.

### Changed
- **Upgrade a Tailwind CSS 4 (`^4.3.5`) + DaisyUI 5 (`^5.8.3`):** Migración a configuración *CSS-first* en `static/css/input.css` (`@import "tailwindcss";` y `@plugin "daisyui"`), actualización de plantillas (`base.html`, `_navbar.html`, `home.html`, `_counter_box.html`, `_modal_demo.html`) y recompilación de `static/css/dist/output.css`.
- **Fijado Django 5.2 LTS:** Acotado `django>=5.2.0,<5.3.0` en `pyproject.toml` y actualizado `uv.lock`.
- **Consolidación Frontend:** Unificación de `django-templates`, `htmx-patterns`, `htmx-alpine`, `django-htmx-components` y `daisyui` en la skill única `django-hypermedia-ui` con referencias bajo demanda (`references/` y `components/`).
- **Documentación renovada:** Actualización integral de `README.md`, `AGENTES.md` y `.agents/skills/README.md` para uso comunitario y asistentes de IA.

### Fixed
- Resuelto conflicto de código de estado en formularios HTMX inválidos, estandarizando **HTTP 200** junto con detección vía `request.htmx` (`django-htmx`) y `@vary_on_headers("HX-Request")`.
- Actualizadas clases utilitarias y de componentes incompatibles tras el salto a Tailwind CSS 4 y DaisyUI 5 (`menu-active`, `alert-soft`, `bg-linear-to-r`, `grow`, `inset-shadow-sm`, `sm:footer-horizontal`, `z-1`).

### Removed
- Eliminado `tailwind.config.js` (reemplazado por configuración CSS-first en `static/css/input.css`).
- Eliminadas 24 skills legadas fragmentadas/redundantes (incluyendo `django-expert`, `celery-patterns` y `django-extensions`) y todas las referencias heredadas a proyectos anteriores.

## [0.1.0] - 2026-11-03

### Added
- Lanzamiento inicial de la plantilla **Django + HTMX + DaisyUI + Alpine.js** (`6f5b69d`) con `uv`, settings divididos por entorno (`config/settings/`), `apps.users.User`, demos HTMX/OOB/modal, `pytest-django` y `ruff`.

[0.3.2]: https://github.com/fquivera/django-starter-template/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/fquivera/django-starter-template/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/fquivera/django-starter-template/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/fquivera/django-starter-template/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/fquivera/django-starter-template/releases/tag/v0.1.0
