# Modular App Packages & Safe Refactoring

Use when an app outgrows flat files (`> 400–500` lines or 4+ models / multiple sub-aggregates).

## Canonical Modular Directory Layout

```text
apps/<app_name>/
├── __init__.py
├── apps.py
├── admin.py
├── models/
│   ├── __init__.py               # Explicit imports + __all__
│   ├── base.py                   # Shared abstract base models / TextChoices
│   └── <aggregate>.py            # Aggregate root + child entities
├── forms/
│   ├── __init__.py
│   └── <aggregate>.py
├── views/
│   ├── __init__.py
│   └── <aggregate>.py
├── urls/
│   ├── __init__.py               # Hub aggregating sub-URLconfs with app_name
│   └── <aggregate>.py
├── services/
│   ├── __init__.py
│   └── <workflow>.py
├── selectors/
│   ├── __init__.py
│   └── <aggregate>.py
├── migrations/
│   └── __init__.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_models.py
    └── test_views.py
```

Group related entities around their Aggregate Root (`Order` + `OrderItem` in `models/orders.py`). Do not create unrelated bounded contexts inside one app—split them into separate `apps/<domain>/` apps instead.

## The `models/__init__.py` Contract

1. **Explicit imports only**: never use `from .orders import *` (Ruff flags undefined symbols).
2. **Dependency order**: import enums and base classes before dependent models.
3. **Explicit `__all__`**: guarantees backward compatibility for `from apps.<app>.models import Model`.

```python
# apps/orders/models/__init__.py
from .base import OrderStatus
from .orders import Order, OrderItem
from .payments import Payment

__all__ = [
    "OrderStatus",
    "Order",
    "OrderItem",
    "Payment",
]
```

### Mitigating Circular Imports

1. **String FKs**: use `"orders.Order"` or `"Order"` in `ForeignKey`, `OneToOneField`, and `ManyToManyField`.
2. **Local/deferred imports**: import sibling models or services inside methods only when needed.
3. **App registry**: inside `apps/<app>/models/`, Django infers `app_label` automatically once re-exported in `models/__init__.py`.

## Services, Selectors, Views & URLs

- **`services/`**: group by use-case workflow, annotate write boundaries with `@transaction.atomic`, re-export public entry points in `services/__init__.py`.
- **`selectors/`**: group reusable read-only queries with `select_related`/`prefetch_related` by aggregate; require explicit `user` / scope arguments.
- **`views/` & `urls/`**: import view callables directly from `..views.<aggregate>` in `urls/<aggregate>.py`; aggregate in `urls/__init__.py` with `app_name = "<app>"`.

## Safe 5-Phase Refactoring Workflow

1. **Baseline**: confirm clean state before editing:
   ```bash
   uv run python manage.py check
   uv run python manage.py makemigrations --check --dry-run
   uv run pytest apps/<app_name>/
   ```
2. **Extract in dependency order**:
   `models/` → `selectors/` & `services/` → `forms/` → `views/` → `urls/`.
3. **Validate after each extraction**:
   ```bash
   uv run python manage.py check
   uv run python manage.py makemigrations --check --dry-run
   uv run pytest apps/<app_name>/
   ```
4. **Stop immediately** if `makemigrations --check --dry-run` detects `DeleteModel` or `CreateModel`: fix `models/__init__.py` exports before proceeding.
5. **Quality Gate**: run `uv run ruff check . && uv run ruff format --check .`.
