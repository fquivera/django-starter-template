---
name: django-security-permissions
description: Security and authorization patterns for Django applications and HTMX partial endpoints. Use when securing views, implementing role-based access control (RBAC), multi-tenancy scoping, row-level object permissions, or preventing IDOR and unauthorized partial swaps.
---

# Django Security & Authorization Patterns

Comprehensive authorization, row-level scoping, and security practices for Django fullstack applications, with specific defenses for HTMX partial endpoints.

---

## 1. Core Rule: No Unchecked Partial Endpoints

Every endpoint that renders an HTML partial or executes a state change must enforce the same authentication and authorization checks as a full-page view.

> [!CAUTION]
> **HTMX URL Obscurity is NOT Security**: An internal endpoint like `/invoices/12/row/` or `/caja/modal/5/` is publicly discoverable in browser network tabs. An authenticated user can forge `GET` or `POST` requests to another user's or organization's IDs (Insecure Direct Object Reference - IDOR).

---

## 2. Multi-Tenancy & Row-Level Authorization

Always scope queries at the QuerySet / Selector level before touching an object.

### 2.1 The Custom QuerySet Pattern for Scoping
Define domain-specific scoping methods on the model's QuerySet:

```python
# apps/billing/models/invoices.py
from django.db import models


class InvoiceQuerySet(models.QuerySet):
    def visible_to(self, user):
        """Scope query to records accessible by the requesting user."""
        if user.is_superuser:
            return self
        if not user.is_authenticated:
            return self.none()
        # Tenant or organization isolation
        return self.filter(organization=user.organization)


class Invoice(models.Model):
    organization = models.ForeignKey("accounts.Organization", on_delete=models.CASCADE)
    objects = InvoiceQuerySet.as_manager()
```

### 2.2 View-Level Retrieval: Prevent IDOR
Never look up an object by `pk` alone without scoping:

```python
# BAD: Vulnerable to IDOR - any user can see/edit any invoice!
invoice = get_object_or_404(Invoice, pk=pk)

# GOOD: Guaranteed row-level isolation
invoice = get_object_or_404(Invoice.objects.visible_to(request.user), pk=pk)
```

For Class-Based Views, always override `get_queryset()`:
```python
class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice

    def get_queryset(self):
        return Invoice.objects.visible_to(self.request.user)
```

---

## 3. Securing HTMX Endpoints

HTMX requests require tailored security and response handling.

### 3.1 CSRF Protection
Every modifying HTMX request (`POST`, `PUT`, `PATCH`, `DELETE`) must carry the CSRF token.

**Option A (Global Header Configuration in `base.html` - Recommended):**
```html
<body hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
```
This automatically attaches the token to all descendant `hx-post` elements without needing manual tokens per button.

**Option B (Form Token):**
```html
<form hx-post="/action/">
    {% csrf_token %}
    ...
</form>
```

### 3.2 Authorization Failures (403 Forbidden with HTMX)
By default, HTMX does not swap responses with 4xx or 5xx status codes. When an unauthorized user attempts an HTMX action:

1. **Option 1: Hard Redirect via `HX-Redirect` Header**
   ```python
   from django.http import HttpResponseForbidden, HttpResponse


   def secure_htmx_action(request, pk):
       if not request.user.has_perm("billing.can_approve_invoice"):
           # Instructs HTMX on the client to perform a full window redirect
           response = HttpResponse(status=403)
           response["HX-Redirect"] = "/access-denied/"
           return response
   ```

2. **Option 2: Error Notification Swap (Toast)**
   ```python
   def secure_inline_action(request, pk):
       if not request.user.has_perm("billing.can_approve_invoice"):
           # Return a 200 with an error alert fragment to swap into the toast container
           return render(request, "common/partials/_unauthorized_toast.html", status=200)
   ```

---

## 4. Role-Based Access Control (RBAC)

Structure permissions using standard Django permissions or custom business capabilities.

### 4.1 Granular Model Permissions
Define explicit business permissions on the model `Meta`:

```python
class Invoice(models.Model):
    class Meta:
        permissions = [
            ("approve_invoice", "Can approve pending invoices"),
            ("export_financials", "Can export financial reports"),
        ]
```

### 4.2 Permission Enforcement in Views
Combine `LoginRequiredMixin` and `PermissionRequiredMixin`:

```python
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import UpdateView


class InvoiceApproveView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "billing.approve_invoice"
    raise_exception = True  # Raises 403 Forbidden instead of redirecting to login

    def get_queryset(self):
        return Invoice.objects.visible_to(self.request.user).filter(status="PENDING")
```

For function views:
```python
from django.contrib.auth.decorators import login_required, permission_required


@login_required
@permission_required("billing.approve_invoice", raise_exception=True)
def approve_invoice_view(request, pk): ...
```

### 4.3 UI Authorization Guarding (Templates)
Never expose action triggers if the user lacks the permission:

```html
{% if perms.billing.approve_invoice and invoice.can_be_approved %}
    <button
        hx-post="{% url 'billing:invoice-approve' invoice.pk %}"
        hx-target="#invoice-status-badge"
        class="btn-success"
    >
        Approve
    </button>
{% endif %}
```
> [!IMPORTANT]
> Template checks (`{% if perms... %}`) are for UX only. The view/service must independently re-validate the permission on request submission.

---

## 5. Security Anti-Patterns to Avoid

- **Trusting Client Data for Ownership**: Never do `Invoice.objects.create(organization_id=request.POST.get("org_id"))`. Always use `request.user.organization`.
- **Relying on `x-show` for Security**: Hiding a button with Alpine (`x-show="isManager"`) does not protect the server endpoint from being requested directly.
- **Unrestricted QuerySets in Selectors**: Selectors must require the requesting `user` or `organization` as an explicit argument (e.g. `get_invoices_for_user(user)`).
- **Ignoring HTTP Method Validation**: In function-based views, always check `if request.method != "POST": return HttpResponseNotAllowed(["POST"])` or use `@require_POST`.

---

## 6. Integration with Other Skills

- **`django-models`**: Attaching `visible_to()` scoping methods to custom QuerySets.
- **`django-patterns`**: Placing cross-aggregate authorization logic in services.
- **`htmx-patterns`**: Django CSRF header integration and HTMX response codes.
- **`django-htmx-components`**: Ensuring modal and inline-edit endpoints enforce row-level checks.
