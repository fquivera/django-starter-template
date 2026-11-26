---
name: django-views-forms-security
description: >
  Thin Django views, ModelForms/formsets, HTMX partial responses (HTTP 200 on form errors), RBAC/IDOR scoping, and i18n strings.
  Use when building or securing endpoints, validating input, or enforcing object-level permissions.
---

# Django Views, Forms & Security

Canonical rules for HTTP endpoints, form validation, row-level isolation (IDOR prevention), RBAC, and baseline i18n.

## 1. RBAC & IDOR Prevention (Non-Negotiable)

- **No unchecked endpoints**: HTMX partial URLs are publicly discoverable in browser devtools and must enforce the exact same auth, RBAC, and row-level checks as full-page views.
- **Scoped retrieval**: Always resolve objects through `Model.objects.visible_to(request.user)` (or tenant/organization scope). Never do `get_object_or_404(Model, pk=pk)` unscoped.
- **CBVs**: Combine `LoginRequiredMixin` + `PermissionRequiredMixin` (`raise_exception = True`) and override `get_queryset()` with `.visible_to(self.request.user)`.
- **Never trust client ownership**: Never assign `user_id` or `organization_id` from `request.POST`; derive ownership from `request.user`.
- **UI guards are UX only**: Hiding buttons with `{% if perms... %}` or Alpine `x-show` never replaces server-side authorization.
- **Explicit HTTP methods**: Use `@require_GET` / `@require_POST` / `require_http_methods` or check `request.method` explicitly.

Detailed RBAC, CBV, and HTMX 403/CSRF snippets: `references/rbac-and-htmx-security.md`.

## 2. Thin Views & HTMX Response Contract

- Views only: authenticate → authorize → validate input → call 1 service/selector → render template/partial.
- Detect HTMX via `request.htmx` (provided by `django-htmx` middleware). When a view returns different templates for HTMX vs full-page requests, decorate with `@vary_on_headers("HX-Request")`.
- **Form validation errors on HTMX**: Re-render the form partial with **HTTP 200** so HTMX swaps it (HTMX ignores 4xx by default; never return 422 unless `htmx.config.responseHandling` is explicitly configured).
- Use `HX-Trigger` for client events/OOB toasts and `HX-Redirect` for full-page redirects after mutations.

## 3. Forms & Validation

- Prefer `ModelForm` for model-backed inputs. Keep validation in forms (`clean_<field>()` for single-field normalization/checks, `clean()` calling `super().clean()` + `self.add_error()` for cross-field rules), never in views.
- Use `form.save(commit=False)` to attach `user`/owner before saving, or pass `form.cleaned_data` into a service function.
- Never put cross-aggregate business rules in `form.clean()`; delegate to services.
- For related collections, use `inlineformset_factory` and validate `form.is_valid() and formset.is_valid()`.
- Always render `form.non_field_errors` and `field.errors` in templates.

## 4. User-Facing Text (i18n Baseline)

- Mark user-facing strings for translation: `gettext_lazy` in models/forms/module constants; `gettext` in views/services; `{% translate %}` / `{% blocktranslate %}` in templates.
- For catalog extraction (`makemessages`/`compilemessages`), localized date/number formatting, and email overrides, read `.agents/skills-ondemand/i18n/SKILL.md`.

## Integration with Other Skills

- `django-architecture`: Layering and modular `views/`/`forms/` packages.
- `django-models-migrations`: Scoped QuerySets (`visible_to`) and model invariants.
- `django-hypermedia-ui`: HTMX/Alpine templates, partials, OOB patterns, DaisyUI 5.
- `django-testing-quality`: Testing permissions, IDOR isolation, and HTMX responses.
