# Zero-Downtime Migrations & PostgreSQL Patterns

Load when writing `RunPython` data migrations, renaming/removing columns, or adding concurrent indexes on live tables.

## Batched `RunPython` Template

Always use `apps.get_model()`, batch with `.iterator(chunk_size=1000)` + `bulk_update()`, and define `reverse_code`:

```python
import uuid
from django.db import migrations


def populate_public_id(apps, schema_editor):
    Order = apps.get_model("orders", "Order")
    batch_size = 1000
    batch = []

    for order in Order.objects.filter(public_id__isnull=True).iterator(
        chunk_size=batch_size
    ):
        order.public_id = uuid.uuid4()
        batch.append(order)
        if len(batch) >= batch_size:
            Order.objects.bulk_update(batch, ["public_id"])
            batch.clear()

    if batch:
        Order.objects.bulk_update(batch, ["public_id"])


def reverse_populate_public_id(apps, schema_editor):
    Order = apps.get_model("orders", "Order")
    Order.objects.all().update(public_id=None)


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0002_order_public_id"),
    ]

    operations = [
        migrations.RunPython(
            populate_public_id,
            reverse_code=reverse_populate_public_id,
        ),
    ]
```

## Safe Column Rename (`db_column`)

Renaming a column directly breaks running application instances during rolling deploys. Keep the DB column name intact while renaming the Python attribute:

```python
class Order(models.Model):
    account_holder = models.ForeignKey(
        "users.User",
        db_column="customer_id",
        on_delete=models.CASCADE,
    )
```

## Non-Blocking PostgreSQL Index (`AddIndexConcurrently`)

`AddIndexConcurrently` avoids an exclusive table write lock and **requires `atomic = False`**:

```python
from django.contrib.postgres.operations import AddIndexConcurrently
from django.db import migrations, models


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("orders", "0003_populate_public_id"),
    ]

    operations = [
        AddIndexConcurrently(
            model_name="order",
            index=models.Index(fields=["created_at"], name="orders_order_created_idx"),
        ),
    ]
```

## Pre-Deploy Verification Commands

```bash
uv run python manage.py makemigrations --check --dry-run
uv run python manage.py migrate --plan
uv run python manage.py sqlmigrate <app_name> <migration_number>
```

Test rollback locally before committing when modifying existing data:

```bash
uv run python manage.py migrate <app_name> <previous_migration_number>
uv run python manage.py migrate <app_name>
```
