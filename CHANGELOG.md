# Changelog

Todos los cambios notables de este proyecto se documentarán en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/), y este proyecto se adhiere a [Semantic Versioning](https://semver.org/lang/es/).

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

[0.2.0]: https://github.com/fquivera/django-starter-template/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/fquivera/django-starter-template/releases/tag/v0.1.0
