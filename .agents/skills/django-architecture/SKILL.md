---
name: django-architecture
description: >
  Django project layering (models/services/selectors/views), modular app packages, and env/settings anti-hardcoding.
  Use when creating apps, placing business logic, splitting flat modules into packages, or adding settings/env vars.
---

# Django Architecture & Configuration

Canonical guide for project layering, modular app packages, and environment configuration in a server-driven Django + HTMX application.

## 1. Layering & Responsibility Boundary

| Logic / Responsibility | Location | Rules |
|---|---|---|
| Row-level invariants, state transitions, derived calculations | `models.py` / `models/` | May raise `ValidationError`. Never send email, call HTTP, or enqueue Huey tasks. Move methods >~10 lines or cross-aggregate workflows to services. |
| Multi-aggregate workflows, transactions, external I/O | `services.py` / `services/` | Own `@transaction.atomic`. Return domain objects, never HTTP responses. Raise domain exceptions. |
| Reusable optimized reads (`select_related`/`prefetch_related`) | `selectors.py` / `selectors/` | Read-only. Always accept explicit `user` or scope argument. |
| HTTP translation (auth, validation, service/selector call, template) | `views.py` / `views/` | Thin only. Zero business rules. |
| Input validation & cleaning | `forms.py` / `forms/` | Validate input in forms, not views. |

For async or scheduled jobs outside the request cycle, read `.agents/skills-ondemand/huey-patterns/SKILL.md`.

## 2. Project Layout & Bounded Contexts

- **Django LTS policy**: pin to **Django 5.2 LTS** (`django>=5.2.0,<5.3.0`) for 3-year production stability and security updates; do not upgrade to non-LTS releases (6.0/6.1) — stay on 5.2 LTS until **Django 6.2 LTS** is released.
- `config/settings/{base,development,test,production}.py` — split settings; never branch on `settings.DEBUG` for business rules or permissions.
- `apps/<domain>/` — one domain noun per app, forming a strict DAG (no circular cross-app imports; use string references like `"orders.OrderItem"` in models).
- `common/` — shared abstract models (e.g. `TimestampedModel`), shared helpers, and context processors.
- Signals: use sparingly (audit logs, cache invalidation). If you control both trigger and reaction, call the service explicitly.

## 3. Flat Files vs. Modular Packages

| Keep flat (`models.py`, `views.py`) | Split into packages (`models/`, `views/`, ...) |
|---|---|
| `< 300–400` lines per file, 1–3 models | `> 400–500` lines or 4+ models / multiple sub-aggregates |

- Group by Aggregate Root (never one tiny file per table).
- Every package `__init__.py` MUST use explicit imports and `__all__` (never `import *`) so Django's app registry and migrations keep working identically.
- Before and after modularizing, verify `uv run python manage.py makemigrations --check --dry-run` produces zero `DeleteModel`/`CreateModel` operations.

Detailed package layout, `__init__.py` templates, and safe 5-phase refactoring checklist: `references/modular-packages.md`.

## 4. Configuration & Anti-Hardcoding

- **Three layers**: Deployment values → env vars (`config/settings/`); Per-user choices → DB preference model; Stable domain constants → `models.TextChoices` or `constants.py`.
- Read env vars exclusively in `config/settings/` via `django-environ` (`env.str`, `env.bool`, `env.int`, `env.list`). Never call `os.environ` or `os.getenv` in `apps/` or `common/`.
- Every new env var must be added to `config/settings/base.py`, `.env.example`, and `references/configuration-rules.md`.
- **Never hardcode**: internal URLs (use `reverse()` / `{% url %}`), static/media paths (`{% static %}` / `MEDIA_ROOT`), raw status strings (use `TextChoices`), or hex/palette colors (use DaisyUI semantic tokens).

Canonical env var table, fail-fast startup checks, and feature flag lifecycle: `references/configuration-rules.md`.

## Integration with Other Skills

- `django-models-migrations`: ORM optimization, custom QuerySets, safe migrations.
- `django-views-forms-security`: Forms, RBAC/IDOR scoping, HTMX view conventions.
- `django-testing-quality`: pytest-django TDD and Ruff Quality Gate.
- `django-hypermedia-ui`: Templates, HTMX/Alpine, Tailwind 4 + DaisyUI 5.
