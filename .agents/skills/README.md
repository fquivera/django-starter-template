# Project Skills

Layered, low-token skill architecture for a modern **Django + HTMX + Alpine.js + Tailwind CSS 4 + DaisyUI 5** project.

## Conventions

1. **Directory name = `name` in frontmatter.**
2. **Frontmatter `description` <= 2 lines** stating *what* it covers and *when* to trigger.
3. **Keep `SKILL.md` lean**; move code templates, long checklists, and component indexes into `references/`.
4. **Write in English**, imperative voice, `uv run ...` commands, and no unrelated stacks (no DRF for internal UI, no Celery).
5. **One owner per topic** — cross-reference instead of duplicating.

## Active Skills (`.agents/skills/` — Auto-Discovered, 6 Total)

### Core (5)

| Skill | Ownership |
|---|---|
| `django-architecture` | Layering (`models`/`services`/`selectors`/`views`), modular app packages, settings & anti-hardcoding |
| `django-models-migrations` | Domain models, N+1-free QuerySets, DB constraints, PostgreSQL zero-downtime migrations |
| `django-views-forms-security` | Thin views, `ModelForm`/formsets, HTMX HTTP 200 form errors, RBAC/IDOR scoping, i18n baseline |
| `django-testing-quality` | `pytest-django` TDD, HTMX/IDOR/Huey test conventions, Ruff/pytest Quality Gate |
| `git-workflow` | GitFlow branches/releases and Conventional Commits |

### Frontend Hypermedia/UI (1 Consolidated Skill)

| Skill | Ownership |
|---|---|
| `django-hypermedia-ui` | Django templates/partials, HTMX + Alpine.js boundaries, Tailwind CSS 4 + DaisyUI 5 components/tokens, inline Heroicons SVGs |

## On-Demand Skills (`.agents/skills-ondemand/` — 0 Tokens by Default)

Read explicitly only when working on these specialized topics:

- `huey-patterns/SKILL.md` — Huey + Redis async and periodic tasks (preferred over Celery)
- `django-infrastructure/SKILL.md` — Docker multi-stage, Gunicorn, Compose, WhiteNoise, Tailwind 4 build, CSP headers
- `django-admin-expert/SKILL.md` — Django Admin N+1 elimination, autocomplete, bulk actions, dynamic permissions
- `github-actions/SKILL.md` — CI/CD workflows, CSS drift check, branch policy, releases
- `i18n/SKILL.md` — Translation catalogs (`.po`/`.mo`), `makemessages`/`compilemessages`, locale formatting
- `systematic-debugging/SKILL.md` — Four-phase root-cause debugging methodology

## Feature Load Order

1. `django-architecture` (where code lives and configuration rules)
2. `django-models-migrations` + `django-views-forms-security` (models, scoped queries, views, forms, permissions)
3. `django-hypermedia-ui` (only when editing HTML templates, HTMX partials, Alpine state, or DaisyUI styles)
4. `django-testing-quality` (TDD tests and mandatory Quality Gate)
5. `git-workflow` (Conventional Commits, branch rules, PRs)
6. `.agents/skills-ondemand/*` (only when touching async tasks, Admin, Docker/CI, i18n catalogs, or deep debugging)
