# RBAC, IDOR Scoping & HTMX Security Patterns

Load when implementing row-level authorization, RBAC permissions, or HTMX error/auth responses.

## 1. Custom QuerySet Scoping (`visible_to`)

Scope queries at the QuerySet / Selector level before any view touches an object:

```python
from django.db import models


class ProjectQuerySet(models.QuerySet):
    def visible_to(self, user):
        if not user.is_authenticated:
            return self.none()
        if user.is_superuser:
            return self
        return self.filter(owner=user)


class Project(models.Model):
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    objects = ProjectQuerySet.as_manager()
```

### View-Level Retrieval (Prevent IDOR)

```python
# BAD: Vulnerable to IDOR
project = get_object_or_404(Project, pk=pk)

# GOOD: Guaranteed row-level isolation
project = get_object_or_404(Project.objects.visible_to(request.user), pk=pk)
```

For Class-Based Views, override `get_queryset()`:

```python
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import UpdateView


class ProjectUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    permission_required = "projects.change_project"
    raise_exception = True  # Return 403 instead of redirecting authenticated users

    def get_queryset(self):
        return Project.objects.visible_to(self.request.user)
```

## 2. Securing HTMX Endpoints

### CSRF Protection

Configure CSRF once on `<body>` in `templates/base.html`:

```html
<body hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
```

Never cache HTML responses containing a user's CSRF token.

### Authorization Failures on HTMX Requests

HTMX does not swap 4xx/5xx responses by default. Handle unauthorized HTMX actions explicitly:

```python
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse


def approve_item(request, pk):
    if not request.user.has_perm("orders.approve_order"):
        if request.htmx:
            response = HttpResponse(status=403)
            response["HX-Redirect"] = reverse("core:home")
            return response
        return HttpResponse(status=403)
```

Alternatively, return an OOB toast alert fragment with HTTP 200 when keeping the user on the current page.

## 3. Thin HTMX Form View Pattern

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.vary import vary_on_headers


@login_required
@vary_on_headers("HX-Request")
def item_create(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            if request.htmx:
                return render(request, "items/partials/_item_row.html", {"item": item})
            return redirect("items:list")
        # Invalid HTMX submission: keep status=200 so HTMX swaps the form with errors
        if request.htmx:
            return render(request, "items/partials/_item_form.html", {"form": form})
    else:
        form = ItemForm()

    template = (
        "items/partials/_item_form.html" if request.htmx else "items/item_create.html"
    )
    return render(request, template, {"form": form})
```
