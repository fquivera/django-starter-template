---
name: django-admin-expert
description: >
  High-performance Django Admin customization: N+1 elimination, autocomplete_fields, bulk atomic actions, and dynamic permissions.
  Use when registering models in admin.py or optimizing backoffice views.
---

# Django Admin Best Practices & Optimization

Patterns for performant, secure backoffice interfaces using Django Admin.

## 1. Zero N+1 Queries in Admin List Views

### 1.1 Use `list_select_related`

Declare `list_select_related` for any `ForeignKey` or `OneToOneField` displayed in `list_display`:

```python
from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("number", "customer", "status", "created_at")
    list_filter = ("status", "created_at")
    list_select_related = ("customer",)
```

### 1.2 Optimize Computed Columns with Annotations

Never run per-row queries inside `@admin.display` methods; annotate in `get_queryset()`:

```python
from django.db.models import Count, Sum


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("number", "item_count", "total_amount")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                _item_count=Count("items", distinct=True),
                _total_amount=Sum("items__amount"),
            )
        )

    @admin.display(ordering="_item_count", description="Items")
    def item_count(self, obj):
        return obj._item_count

    @admin.display(ordering="_total_amount", description="Total")
    def total_amount(self, obj):
        return obj._total_amount or 0
```

### 1.3 Disable Full Table Counts on Large Datasets

```python
class LargeTableAdmin(admin.ModelAdmin):
    show_full_result_count = False
```

## 2. Autocomplete Fields & Efficient Inlines

```python
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ("name", "email")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    autocomplete_fields = ("product",)
    fields = ("product", "quantity", "unit_price")
```

## 3. Safe Bulk Admin Actions

Wrap bulk actions in `transaction.atomic()` and report clear feedback with `self.message_user`:

```python
from django.contrib import admin, messages
from django.db import transaction


@admin.action(description="Approve selected pending orders", permissions=["change"])
def approve_orders(modeladmin, request, queryset):
    pending = queryset.filter(status="PENDING")
    count = pending.count()
    if count == 0:
        modeladmin.message_user(
            request, "No pending orders selected.", level=messages.WARNING
        )
        return

    with transaction.atomic():
        for order in pending:
            order.approve(approved_by=request.user)

    modeladmin.message_user(
        request, f"Approved {count} order(s).", level=messages.SUCCESS
    )
```

## 4. Dynamic Permissions & Field Locking

```python
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if obj and obj.status in ("PAID", "CANCELLED"):
            return [field.name for field in obj._meta.fields]
        return readonly

    def has_delete_permission(self, request, obj=None):
        if obj and obj.payments.exists():
            return False
        return super().has_delete_permission(request, obj)
```

## Integration with Other Skills

- `django-models-migrations`: Proper `__str__()` and indexes supporting `search_fields`.
- `django-views-forms-security`: Aligning backoffice permissions with domain RBAC.
