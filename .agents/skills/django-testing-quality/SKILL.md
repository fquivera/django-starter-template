---
name: django-testing-quality
description: >
  pytest-django TDD patterns, HTMX/IDOR/Huey test conventions, and the uv/Ruff/pytest Quality Gate.
  Use when writing or fixing tests, creating fixtures, or auditing code quality before commit.
---

# Django Testing & Code Quality

Canonical guide for TDD with `pytest-django`, isolation testing, and the mandatory project Quality Gate.

## 1. TDD Cycle (RED → GREEN → REFACTOR)

1. **RED**: Write a failing test reproducing the bug or specifying the new behavior before editing production code.
2. **GREEN**: Write minimal code to make the test pass.
3. **REFACTOR**: Clean up structure and naming while keeping tests green.

## 2. pytest-django Conventions

- Mark DB tests with `@pytest.mark.django_db` (or module-level `pytestmark = pytest.mark.django_db`).
- Put shared fixtures (`auth_client`, `user`, test helpers) in `conftest.py` (or `apps/<app>/tests/conftest.py`). Name tests `test_<action>_<expected_outcome>`, group in `Test<Component>` classes, use `@pytest.mark.parametrize` for variants, and mock only external I/O (`monkeypatch` / `unittest.mock.patch`).
- **Always test**:
  - **IDOR / Ownership**: cross-user or unauthorized access returns 404/403.
  - **RBAC**: unauthorized roles/permissions rejected, authorized succeed.
  - **HTMX**: pass `HTTP_HX_REQUEST="true"`, assert partial template rendered, `Vary` includes `HX-Request` when response varies, and **HTTP 200** on form validation errors.
  - **Models & Services**: invariants, constraints, `@transaction.atomic` rollbacks, and N+1 avoidance (`django_assert_num_queries`).
  - **Huey tasks** (when used): run synchronously with `HUEY_IMMEDIATE=True` in `config/settings/test.py`, pass primitive IDs only, verify idempotency.

Pytest shortcuts, fixture patterns, and manual code-review checklist: `references/fixtures-and-checklist.md`.

## 3. Quality Gate (Mandatory Before Finishing)

```bash
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

If templates or CSS changed, also run `npm run build:css`.

## Integration with Other Skills

- `django-views-forms-security`: RBAC/IDOR and HTMX view contracts under test.
- `django-models-migrations`: QuerySets, constraints, and migration dry-run checks.
- `git-workflow`: Pre-PR checks and Conventional Commits.
- `.agents/skills-ondemand/systematic-debugging/SKILL.md`: Root-cause debugging for persistent failures.
