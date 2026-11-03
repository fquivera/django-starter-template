---
name: django-migrations-patterns
description: Safe database schema evolution, data migrations, and zero-downtime practices for Django. Use when writing data migrations (RunPython), adding non-nullable columns, renaming fields/models, creating concurrent indexes, or planning zero-downtime deployments.
---

# Django Migrations & Schema Evolution Patterns

Production guidelines for writing safe, reversible, and zero-downtime database migrations in Django.

---

## 1. Golden Rules of Migrations

1. **NEVER Import Live Models**: Inside a migration file, never write `from apps.billing.models import Invoice`. Always use `apps.get_model("billing", "Invoice")`. Live models reflect the current codebase, which will break historical migrations when fields are added or removed in future releases.
2. **Always Provide a Reverse Operation**: Every `RunPython` and `RunSQL` operation must specify both forward and reverse functions: `migrations.RunPython(forward_func, reverse_func)`.
3. **Keep Schema and Data Migrations Separate**: Do not create or alter tables and populate heavy data within the exact same migration file. Split them into two consecutive migrations.

---

## 2. Safe Data Migrations (`RunPython`)

When migrating, transforming, or backfilling data:

### 2.1 The Canonical Data Migration Template
```python
# apps/billing/migrations/0005_populate_invoice_uuid.py
import uuid
from django.db import migrations


def populate_invoice_uuid(apps, schema_editor):
    Invoice = apps.get_model("billing", "Invoice")
    # Batch updates to prevent memory exhaustion and table locks
    batch_size = 1000
    invoices_to_update = []

    for invoice in Invoice.objects.filter(uuid__isnull=True).iterator(
        chunk_size=batch_size
    ):
        invoice.uuid = uuid.uuid4()
        invoices_to_update.append(invoice)

        if len(invoices_to_update) >= batch_size:
            Invoice.objects.bulk_update(invoices_to_update, ["uuid"])
            invoices_to_update.clear()

    if invoices_to_update:
        Invoice.objects.bulk_update(invoices_to_update, ["uuid"])


def reverse_populate_invoice_uuid(apps, schema_editor):
    Invoice = apps.get_model("billing", "Invoice")
    Invoice.objects.all().update(uuid=None)


class Migration(migrations.Migration):
    dependencies = [
        ("billing", "0004_invoice_uuid"),
    ]

    operations = [
        migrations.RunPython(
            populate_invoice_uuid,
            reverse_code=reverse_populate_invoice_uuid,
        ),
    ]
```

---

## 3. Zero-Downtime Schema Evolution

In production systems with live traffic, naive schema migrations can lock tables or cause operational downtime. Follow the three-phase expand/contract pattern:

### 3.1 Adding a Non-Nullable Field (`NOT NULL`)
Directly adding a `NOT NULL` column without a default locks large tables and fails if existing rows exist.

* **Phase 1 (Release N)**: Add the field as nullable (`null=True, blank=True`).
* **Phase 2 (Release N)**: Run a data migration (`RunPython`) to populate default values for all existing rows.
* **Phase 3 (Release N+1)**: Alter the field to `null=False` with `models.AlterField`.

### 3.2 Renaming a Field
Renaming a field in Django (`python manage.py makemigrations`) executes an SQL column rename, breaking running application servers during rolling deployments.

**Zero-Downtime Solution:**
Keep the underlying database column name unchanged using `db_column`:
```python
# In models.py
class Invoice(models.Model):
    # Renamed attribute in Python, but underlying column stays the same in Postgres!
    customer_account = models.ForeignKey(
        "accounts.Account",
        db_column="client_id",  # Matches the existing column
        on_delete=models.CASCADE,
    )
```

### 3.3 Deleting a Field
* **Step 1**: Remove all code references to the field in views, forms, and services. Set `editable=False, blank=True, null=True` in the model. Deploy.
* **Step 2**: In the following deployment release, remove the field from `models.py` and run `makemigrations`.

---

## 4. PostgreSQL Performance: Non-Blocking Index Creation

Creating an index on a table with hundreds of thousands of rows will take an exclusive table lock by default. In PostgreSQL, use concurrent index creation:

```python
# apps/billing/migrations/0006_add_invoice_date_idx_concurrently.py
from django.contrib.postgres.operations import AddIndexConcurrently
from django.db import migrations, models


class Migration(migrations.Migration):
    # CRITICAL: atomic must be False for PostgreSQL CONCURRENTLY operations
    atomic = False

    dependencies = [
        ("billing", "0005_populate_invoice_uuid"),
    ]

    operations = [
        AddIndexConcurrently(
            model_name="invoice",
            index=models.Index(fields=["created_at"], name="billing_inv_created_idx"),
        ),
    ]
```

---

## 5. Verification Checklist Before Deployment

Before pushing a branch with migrations:

1. **Dry-Run Check**:
   ```bash
   uv run python manage.py makemigrations --check --dry-run
   ```
   Ensures no model changes were left without a migration file.

2. **Migration Plan Review**:
   ```bash
   uv run python manage.py migrate --plan
   ```
   Inspects the exact order of operations.

3. **Rollback Test (Local Verification)**:
   Always test that the migration can roll back and re-apply cleanly:
   ```bash
   uv run python manage.py migrate <app_name> <previous_migration_number>
   uv run python manage.py migrate <app_name>
   ```

---

## 6. Integration with Other Skills

- **`django-models`**: Aligning model field types and indexes before generating migrations.
- **`django-modular-apps`**: Ensuring `models/__init__.py` exposes all models so migrations never generate accidental `DeleteModel` operations.
- **`django-infrastructure`**: Applying migrations safely during production container rollout.
