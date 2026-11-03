---
name: django-modular-apps
description: Patterns and rules for modularizing Django applications into package-based submodules (models/, views/, forms/, urls/, services/, selectors/). Use when an application grows beyond flat files, refactoring monolithic components, or designing multi-aggregate domain apps.
---

# Django Modular App Patterns

Guidance for structuring medium-to-large Django applications into cohesive, package-based submodules while preserving backward compatibility, avoiding circular imports, and maintaining clear boundaries.

---

## 1. Decision Matrix: Flat Files vs Modular Packages

Django defaults to flat files (`models.py`, `views.py`, `forms.py`, `urls.py`). Splitting too early causes unnecessary boilerplate and navigation friction; splitting too late leads to unwieldy monoliths with merge conflicts.

Use this decision matrix:

| Metric / Dimension | Keep Flat Files (`models.py`, `views.py`) | Transition to Modular Packages (`models/`, `views/`) |
|---|---|---|
| **File Line Count** | `< 300 - 400` lines per component | `> 400 - 500` lines in any single file |
| **Domain Entities** | 1–3 simple, tightly coupled models | 4+ models or multiple distinct sub-aggregates |
| **Business Complexity** | Simple CRUD, few custom QuerySets/actions | Multi-step workflows, distinct transactional units |
| **Team Concurrency** | 1 developer editing the app at a time | Multiple developers actively modifying the app |

> [!IMPORTANT]
> **Bounded Context Check**: Do not use subpackages to mask domain bleed. If an app contains unrelated business concepts (e.g. Mixing customer billing and support ticketing in one app), split them into separate Django apps (`apps/billing/` and `apps/support/`), not just subpackages inside one app. Subpackages are for multiple aggregates belonging to the **same** domain.

---

## 2. Canonical Directory Layout

When an application qualifies for modularization, replace flat files with Python packages (directories with `__init__.py`). Each subpackage mirrors domain concepts:

```text
apps/billing/
├── __init__.py
├── apps.py
├── admin.py
├── models/
│   ├── __init__.py               # Re-exports all models with __all__
│   ├── base.py                   # Shared abstract base models / enums
│   ├── invoices.py               # Invoice, InvoiceItem
│   └── payments.py               # Payment, PaymentAttempt, Refund
├── forms/
│   ├── __init__.py               # Re-exports forms or submodules
│   ├── invoices.py               # InvoiceForm, InvoiceFilterForm
│   └── payments.py               # PaymentMethodForm, RefundForm
├── views/
│   ├── __init__.py               # Re-exports public views
│   ├── invoices.py               # InvoiceListView, InvoiceDetailView
│   └── payments.py               # PaymentProcessView, PaymentWebhookView
├── urls/
│   ├── __init__.py               # Root router aggregating sub-URLconfs
│   ├── invoices.py               # /invoices/... routes
│   └── payments.py               # /payments/... routes
├── services/
│   ├── __init__.py               # Re-exports domain services
│   ├── invoice_creation.py       # Invoice creation & line-item calculations
│   └── payment_gateway.py        # Gateway charge orchestrator
├── selectors/
│   ├── __init__.py               # Re-exports reusable queries
│   ├── invoices.py               # get_unpaid_invoices_for_account()
│   └── payments.py               # get_payment_summary()
├── migrations/
│   └── __init__.py
└── tests/
    ├── __init__.py
    ├── factories.py
    ├── test_models.py
    └── test_views.py
```

### Granularity Rule: Group by Aggregate Root
Never create a file per database table if tables are small (e.g. avoid creating 20 files of 15 lines). Group related entities around their Aggregate Root (e.g. `Invoice` + `InvoiceItem` live together in `models/invoices.py`).

---

## 3. Package Implementation Patterns

### 3.1 Models Package (`models/`)

Django discovers models through the app registry. When converting `models.py` to `models/`, the package must behave identically to the single file.

#### The `models/__init__.py` Contract
1. **Explicit Imports**: Never use wildcard imports (`from .invoices import *`). Linters like Ruff flag undefined symbols and star imports obscure source locations.
2. **Strict Import Order**: Import dependencies before dependents (e.g., base configurations and enums first, transactional models last).
3. **Explicit `__all__`**: Define `__all__` listing every model name to guarantee 100% backward compatibility for consumers doing `from apps.billing.models import Invoice`.

```python
# apps/billing/models/__init__.py
"""
Billing domain models.
Exposed via __all__ for seamless backward compatibility.
"""

from .base import BillingStatus, Currency
from .invoices import Invoice, InvoiceItem
from .payments import Payment, PaymentAttempt, Refund

__all__ = [
    # Base / Enums
    "BillingStatus",
    "Currency",
    # Invoices
    "Invoice",
    "InvoiceItem",
    # Payments
    "Payment",
    "PaymentAttempt",
    "Refund",
]
```

#### Mitigating Circular Dependencies
Submodules within `models/` often reference each other. Prevent circular import deadlocks using these three rules:

1. **String References in Relations**: Always use string references for `ForeignKey`, `OneToOneField`, and `ManyToManyField`:
   ```python
   # apps/billing/models/payments.py
   from django.db import models


   class Payment(models.Model):
       # Good: String reference prevents circular import
       invoice = models.ForeignKey(
           "billing.Invoice",  # or 'Invoice' within same app
           on_delete=models.CASCADE,
           related_name="payments",
       )
   ```
2. **Local/Deferred Imports**: When a model method needs to call another model or a service, import locally inside the method:
   ```python
   # apps/billing/models/invoices.py
   class Invoice(models.Model):
       def create_payment_attempt(self, amount):
           from .payments import PaymentAttempt

           return PaymentAttempt.objects.create(invoice=self, amount=amount)
   ```
3. **Explicit `app_label`**: If models reside in non-standard nested directories, declare `app_label` in `Meta`. Within standard `apps/<app_name>/models/`, Django infers `app_label` automatically.

---

### 3.2 Services & Selectors Packages (`services/` & `selectors/`)

Per `django-models` and `django-infrastructure`, business logic orchestration belongs in `services` and reusable reads belong in `selectors`.

#### Services (`services/`)
Organize services by use-case workflows. Each submodule contains focused functions or classes:

```python
# apps/billing/services/invoice_creation.py
from decimal import Decimal
from django.db import transaction
from ..models import Invoice, InvoiceItem


@transaction.atomic
def create_invoice_with_items(*, customer_id: int, items_data: list[dict]) -> Invoice:
    invoice = Invoice.objects.create(customer_id=customer_id)
    for item in items_data:
        InvoiceItem.objects.create(
            invoice=invoice,
            description=item["description"],
            amount=Decimal(item["amount"]),
        )
    return invoice
```

Export key service functions in `services/__init__.py` to provide a clean entry point:
```python
# apps/billing/services/__init__.py
from .invoice_creation import create_invoice_with_items
from .payment_gateway import process_credit_card_charge

__all__ = [
    "create_invoice_with_items",
    "process_credit_card_charge",
]
```

#### Selectors (`selectors/`)
Keep read-only optimized queries (with necessary `select_related`/`prefetch_related`) grouped by aggregate:

```python
# apps/billing/selectors/invoices.py
from django.db.models import QuerySet
from ..models import Invoice, BillingStatus


def get_overdue_invoices_for_customer(customer_id: int) -> QuerySet[Invoice]:
    return (
        Invoice.objects.filter(customer_id=customer_id, status=BillingStatus.OVERDUE)
        .select_related("customer")
        .prefetch_related("items")
    )
```

---

### 3.3 Views & Forms Packages (`views/` & `forms/`)

Group views and forms in parallel to the domain aggregates:

1. **Forms**: Place form classes corresponding to the aggregate in `forms/<aggregate>.py`.
2. **Views**: Group class-based views or HTMX endpoints in `views/<aggregate>.py`.
3. **Explicit View Imports in URLs**: Prefer importing views directly from their submodules inside URLconfs rather than importing from a monolithic views init:
   ```python
   # apps/billing/urls/invoices.py
   from django.urls import path
   from ..views.invoices import (
       InvoiceListView,
       InvoiceDetailView,
       htmx_invoice_row,
   )

   urlpatterns = [
       path("", InvoiceListView.as_view(), name="invoice-list"),
       path("<int:pk>/", InvoiceDetailView.as_view(), name="invoice-detail"),
       path("<int:pk>/row/", htmx_invoice_row, name="invoice-row"),
   ]
   ```

---

### 3.4 URLs Package (`urls/`)

For complex apps with 20+ routes, modularize `urls/` using the hub-and-spoke pattern:

```python
# apps/billing/urls/__init__.py
"""
Billing URL routing hub.
Aggregates sub-URLconfs for each domain aggregate.
"""

from django.urls import path, include

app_name = "billing"

urlpatterns = [
    path("invoices/", include("apps.billing.urls.invoices")),
    path("payments/", include("apps.billing.urls.payments")),
]
```

*Note*: If URLs share the root path without separate URL prefixes, use `path("", include("apps.billing.urls.invoices"))`.

---

## 4. Safe Refactoring Workflow (Step-by-Step)

When refactoring an existing flat Django app to a modular package, follow this zero-downtime, verified workflow:

### Phase 1: Baseline Verification
Before touching files, ensure existing tests pass and migration state is clean:
```bash
uv run python manage.py check
uv run python manage.py makemigrations --dry-run
uv run pytest apps/<app_name>/
```

### Phase 2: Create Safety Backups
Temporarily rename flat files as backups:
```bash
cp apps/<app_name>/models.py apps/<app_name>/models_old.py
cp apps/<app_name>/views.py apps/<app_name>/views_old.py
cp apps/<app_name>/forms.py apps/<app_name>/forms_old.py
cp apps/<app_name>/urls.py apps/<app_name>/urls_old.py
```

### Phase 3: Extraction Order
Refactor components in dependency order to prevent circular errors:
1. **Models**: Create `models/` directory, split into domain files, create `models/__init__.py` with full `__all__`. Remove `models.py`.
2. **Selectors & Services**: Extract queries to `selectors/` and orchestration to `services/`.
3. **Forms**: Create `forms/` directory, split by model/feature, create `forms/__init__.py`. Remove `forms.py`.
4. **Views**: Create `views/` directory, split views by workflow, create `views/__init__.py`. Remove `views.py`.
5. **URLs**: Create `urls/` directory, split route definitions, aggregate in `urls/__init__.py`. Remove `urls.py`.

### Phase 4: Validation Gate
Run checks immediately after each extraction:
```bash
# 1. Check for Python syntax or import errors
uv run python manage.py check

# 2. Crucial: Ensure Django does not think models were deleted/recreated!
# Expected output: "No changes detected in app '<app_name>'"
uv run python manage.py makemigrations --dry-run

# 3. Verify application tests pass
uv run pytest apps/<app_name>/
```

> [!CAUTION]
> If `makemigrations --dry-run` generates `DeleteModel` or `CreateModel` operations, models were not properly re-exported in `models/__init__.py` or model class names were altered. Fix imports immediately before running tests or migrations.

### Phase 5: Cleanup
Once all checks and tests pass, remove the temporary `*_old.py` files:
```bash
rm apps/<app_name>/*_old.py
```

---

## 5. Integration with Other Skills

- **`django-models`**: Single source of truth for row-level logic, QuerySet managers, and model/service boundaries.
- **`django-patterns`**: Overall project layout and routing between architectural layers.
- **`django-infrastructure`**: Production deployment, settings separation, and app-level Bounded Contexts.
- **`django-forms`**: Detailed form validation rules and HTMX error handling.
- **`pytest-django-patterns`**: Writing test fixtures and isolated tests for modular packages.
