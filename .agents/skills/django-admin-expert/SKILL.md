---
name: django-admin-expert
description: High-performance Django Admin customization and backoffice workflows. Use when registering models, optimizing Admin queries (avoiding N+1), creating bulk admin actions, configuring inlines with autocomplete, or restricting fields dynamically by role and object state.
---

# Django Admin Best Practices & Optimization

Patterns for building performant, secure, and user-friendly backoffice interfaces using the Django Admin.

---

## 1. Zero N+1 Queries in Admin List Views

Default admin list views often trigger hundreds of database queries when displaying related fields.

### 1.1 Use `list_select_related`
Always declare `list_select_related` for any `ForeignKey` or `OneToOneField` displayed in `list_display`:

```python
# apps/billing/admin.py
from django.contrib import admin
from .models import Invoice, InvoiceItem


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("number", "customer", "status", "created_at", "total_amount")
    list_filter = ("status", "created_at")

    # CRITICAL: Performs SQL JOINs, preventing 1 query per row for 'customer'
    list_select_related = ("customer", "organization")
```

### 1.2 Optimize Computed List Display Columns
Never run queries inside custom `@admin.display` methods. Instead, annotate the value in `get_queryset()`:

```python
from django.db.models import Count, Sum


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("number", "item_count", "total_amount")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Compute counts at the database level in a single query
        return qs.annotate(
            _item_count=Count("items", distinct=True),
            _total_amount=Sum("items__amount"),
        )

    @admin.display(ordering="_item_count", description="Items")
    def item_count(self, obj):
        return obj._item_count

    @admin.display(ordering="_total_amount", description="Total Amount")
    def total_amount(self, obj):
        return f"${obj._total_amount or 0:.2f}"
```

### 1.3 Disable Full Table Counts on Large Datasets
On tables with > 50,000 rows, `SELECT COUNT(*)` on every page load slows down PostgreSQL:

```python
class LargeTableAdmin(admin.ModelAdmin):
    # Prevents expensive COUNT(*) queries on list view
    show_full_result_count = False
```

---

## 2. Autocomplete Fields & Efficient Inlines

Avoid dropdown selects that load thousands of database records into an HTML `<select>`.

### 2.1 Autocomplete Instead of Raw Selects
```python
# 1. Target admin MUST declare search_fields
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ("name", "tax_id", "email")


# 2. Referencing admin uses autocomplete_fields
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    autocomplete_fields = ("customer",)
```

### 2.2 TabularInline Optimization
```python
class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0  # Do not render empty extra forms by default
    min_num = 0
    autocomplete_fields = ("product",)
    fields = ("product", "quantity", "unit_price", "subtotal")
    readonly_fields = ("subtotal",)
```

---

## 3. Safe Bulk Admin Actions

Bulk actions run over `queryset` selections. Always wrap them in transactions and log clear messages:

```python
from django.contrib import admin, messages
from django.db import transaction


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    actions = ["mark_as_approved"]

    @admin.action(
        description="Approve selected pending invoices", permissions=["change"]
    )
    def mark_as_approved(self, request, queryset):
        pending_invoices = queryset.filter(status="PENDING")
        count = pending_invoices.count()

        if count == 0:
            self.message_user(
                request,
                "No pending invoices were eligible for approval.",
                level=messages.WARNING,
            )
            return

        with transaction.atomic():
            # Trigger custom service or bulk update
            for invoice in pending_invoices:
                invoice.approve(approved_by=request.user)

        self.message_user(
            request,
            f"Successfully approved {count} invoice(s).",
            level=messages.SUCCESS,
        )
```

---

## 4. Dynamic Permissions & Field Locking

Lock fields dynamically depending on user role or business state (e.g. Do not allow editing an invoice once paid):

```python
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if obj and obj.status in ("PAID", "CANCELLED"):
            # Freeze all fields once the invoice is finalized
            return [field.name for field in obj._meta.fields]
        return readonly

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion if record has financial transactions
        if obj and obj.payments.exists():
            return False
        return super().has_delete_permission(request, obj)
```

---

## 5. Integration with Other Skills

- **`django-models`**: Ensuring models have clear string representations (`__str__`) and proper database indexes for `search_fields`.
- **`django-security-permissions`**: Aligning Admin permissions with domain RBAC.
- **`django-forms`**: Customizing Admin form widgets and clean validation methods.
