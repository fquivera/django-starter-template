---
name: i18n
description: >
  Django internationalization: gettext/gettext_lazy, template translation tags, LocaleMiddleware, catalog compilation (.po/.mo), and localized formatting.
  Use when extracting translation catalogs, adding multi-language switching, or formatting dates/numbers per locale.
---

# Internationalization (i18n)

## 1. Core Principles

- Mark all user-facing strings for translation (`gettext_lazy` in models/forms/module-level constants; `gettext` in runtime views/services; `{% translate %}` / `{% blocktranslate %}` in templates).
- Keep logs, audit keys, URL names, and DB enum codes untranslated; translate only user-facing display labels.
- Never concatenate translated fragments (`_("Hello ") + name`); use named placeholders (`%(name)s`) so translators can reorder sentences.
- Never interpolate `gettext_lazy` objects directly in f-strings (`str(_lazy("..."))` if forced).

## 2. Settings & Middleware

```python
# config/settings/base.py
LANGUAGE_CODE = env.str("DJANGO_LANGUAGE_CODE", default="es-ve")
LANGUAGES = [("es", "Español"), ("en", "English")]
LOCALE_PATHS = [BASE_DIR / "locale"]
USE_I18N = True
USE_TZ = True
```

Place `django.middleware.locale.LocaleMiddleware` after `SessionMiddleware` and before `CommonMiddleware`.

## 3. Python & Template APIs

```python
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _lazy
from django.utils.translation import ngettext, pgettext


# Models / Forms (import time)
class Status(models.TextChoices):
    OPEN = "open", _lazy("Open")


# Views / Services (runtime)
message = ngettext("%(count)s item", "%(count)s items", count) % {"count": count}
label = pgettext("verb", "Post")
```

```django
{% load i18n %}

<h1>{% translate "Dashboard" %}</h1>

{% blocktranslate trimmed with count=items|length %}
  Showing {{ count }} record.
{% plural %}
  Showing {{ count }} records.
{% endblocktranslate %}
```

- Use `{% get_current_language as LANGUAGE_CODE %}` for `<html lang="{{ LANGUAGE_CODE }}">`.
- For emails or background tasks (Huey), wrap rendering in `with translation.override(user.language):`.

## 4. Dates, Numbers & JavaScript

- Keep `USE_TZ = True`; store UTC in the database and format in templates with localized formats (`{{ value|date:"SHORT_DATE_FORMAT" }}`, `{{ value|floatformat }}`).
- For client-side Alpine strings, pass translated labels via `data-*` attributes or `{{ translations|json_script:"i18n" }}` (CSP-safe, no inline script concatenation).

## 5. Translation Catalogs

Requires GNU gettext (`xgettext`, `msgfmt`) when regenerating catalogs:

```bash
uv run python manage.py makemessages -l es --ignore=.venv --ignore=node_modules
uv run python manage.py compilemessages
```

Commit both `django.po` and compiled `django.mo` files so runtime images do not need gettext installed.

## 6. Testing Translations

```python
from django.utils import translation


def test_validation_error_translated(client):
    with translation.override("es"):
        response = client.post(reverse("users:login"), {})
    assert response.status_code == 200
```

## Integration with Other Skills

- `django-views-forms-security`: Baseline i18n rules in views and forms.
- `django-hypermedia-ui`: Translated HTMX partials and template tags.
