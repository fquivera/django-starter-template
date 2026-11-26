---
name: systematic-debugging
description: >
  Four-phase root-cause debugging methodology for Django, HTMX, ORM queries, and Huey tasks.
  Use when investigating persistent bugs, failing tests, N+1 regressions, or unexpected behavior.
---

# Systematic Debugging for Django

## Core Principle: NO FIXES WITHOUT ROOT CAUSE FIRST

Never apply speculative patches that mask symptoms. Understand why something fails before editing production code.

## Four-Phase Framework

### Phase 1: Reproduce and Investigate

1. **Write a failing test** capturing the bug (`@pytest.mark.django_db`).
2. **Read the full traceback and error output** carefully.
3. **Inspect recent changes**: `git diff`, `git log -n 5`.
4. **Trace the data flow** across view → form → service/selector → model.

### Phase 2: Isolate

Narrow down state with strategic logging or `breakpoint()`:

```python
import logging

logger = logging.getLogger(__name__)
logger.debug("Method=%s HTMX=%s User=%s", request.method, request.htmx, request.user)
```

Drop into `pdb` on first test failure:

```bash
uv run pytest --pdb -x
```

### Phase 3: Identify Root Cause

- Inspect SQL queries with `CaptureQueriesContext(connection)` or `django_assert_num_queries`.
- Verify HTMX request/response headers (`hx-target`, `hx-swap`, `HX-Request`, HTTP status code—remember HTMX ignores 4xx by default).
- Debug Huey tasks synchronously by setting `HUEY_IMMEDIATE=True` or calling the underlying service function directly.
- Inspect migration state with `uv run python manage.py showmigrations` and `migrate --plan`.

### Phase 4: Fix and Verify

1. Implement the minimal fix at the root cause.
2. Confirm the reproduction test passes.
3. Run the full Quality Gate:

```bash
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

## Red Flags

Stop and escalate/re-analyze if you catch yourself thinking:
- *"Quick fix now, investigate later."*
- *"One more tweak"* after 2–3 failed attempts (indicates a wrong assumption or architectural issue).

## Integration with Other Skills

- `django-testing-quality`: Write the failing regression test first and run the Quality Gate.
- `django-models-migrations`: Resolve QuerySet N+1s and migration mismatches.
- `django-hypermedia-ui`: Diagnose HTMX swaps, `Vary`, and Alpine state issues.
- `.agents/skills-ondemand/huey-patterns/SKILL.md`: Debug async tasks with `HUEY_IMMEDIATE=True`.
