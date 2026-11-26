---
name: django-models-migrations
description: >
  Django ORM modeling, N+1-free custom QuerySets, DB constraints, and zero-downtime PostgreSQL migrations.
  Use when designing models, optimizing queries, or writing RunPython data migrations and concurrent indexes.
---

# Django Models, ORM & Safe Migrations

Canonical rules for domain modeling, QuerySet composition, ORM performance, and PostgreSQL-safe migrations.

## 1. Domain Model Design

- Business models inherit shared abstract bases (e.g. `TimestampedModel`); always define `class Meta` with `ordering`, `verbose_name`, `constraints`, and `indexes`.
- Reference the user model via `settings.AUTH_USER_MODEL` (never import `apps.users.models.User` directly) and use string FKs across apps (`"orders.OrderItem"`).
- Use `models.TextChoices`/`IntegerChoices` for statuses and enums; implement `__str__()` and `get_absolute_url()`.
- Optional text fields: `blank=True, default=""` (avoid `null=True` unless `unique=True`). Optional FKs: `null=True, blank=True`.
- Encapsulate single-row invariants and calculations in model methods (`order.can_cancel()`, `invoice.calculate_total()`). Pass `update_fields=[...]` on partial saves.
- Cross-aggregate orchestration, `@transaction.atomic` workflows, email, external HTTP calls, or Huey enqueueing belong in `services.py`, never in model methods.

## 2. Custom QuerySets & N+1 Prevention

- Prefer custom `QuerySet` attached via `objects = MyQuerySet.as_manager()` for chainable domain filters (`visible_to(user)`, `active()`, `recent()`). Use a custom `Manager` only for factory methods (`create_user()`).
- **`select_related()`** for FK / OneToOne (SQL JOIN); **`prefetch_related()`** (or `Prefetch(...)`) for reverse FK / M2M.
- Use `.exists()` instead of `if qs:`, `.count()` instead of `len(qs)`, `only()`/`defer()` for wide tables, and `F()`/`annotate()`/`aggregate()` for DB-level math.
- Enforce DB-level integrity with `UniqueConstraint` and `CheckConstraint` in `Meta.constraints`.

## 3. Safe Migrations & Schema Evolution

- **Never import live models** in migrations — always use `apps.get_model("app_label", "ModelName")`.
- **Always provide `reverse_code`** on `RunPython` / `RunSQL`.
- **Separate schema and data migrations** into consecutive files; batch `RunPython` updates with `.iterator(chunk_size=1000)` + `bulk_update()`.
- **Zero-downtime expand/contract**:
  - New `NOT NULL` field: (1) add nullable → (2) backfill via `RunPython` → (3) `AlterField(null=False)`.
  - Rename column safely: keep `db_column="old_name"` on the renamed Python attribute.
  - Delete field: remove code refs & make nullable first; drop column in next release.
- **PostgreSQL concurrent indexes**: use `AddIndexConcurrently` with `atomic = False` on the `Migration` class.
- Generate with `uv run python manage.py makemigrations`; **never run `migrate` without explicit user instruction**. Verify with `uv run python manage.py makemigrations --check --dry-run`.

Full `RunPython` batched template, `db_column` rename, and `AddIndexConcurrently` examples: `references/zero-downtime-migrations.md`.

## Integration with Other Skills

- `django-architecture`: Layering boundary and modular `models/` packages.
- `django-views-forms-security`: Scoping QuerySets (`visible_to`) to prevent IDOR.
- `django-testing-quality`: Testing models, constraints, and QuerySets with `pytest-django`.
