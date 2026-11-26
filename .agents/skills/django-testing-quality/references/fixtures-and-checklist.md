# Pytest Fixtures, Shortcuts & Code Review Checklist

## Common `pytest` Commands

```bash
uv run pytest                        # Full test suite
uv run pytest -x                     # Stop on first failure
uv run pytest --lf                   # Re-run last failed tests
uv run pytest apps/core/             # Test a single app
uv run pytest -k "htmx"              # Filter by test name
uv run pytest --cov=apps             # Coverage report
```

## Reusable `conftest.py` Fixtures

```python
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="alice",
        email="alice@example.com",
        password="test-password-123",
    )


@pytest.fixture
def auth_client(client, user):
    client.force_login(user)
    return client


@pytest.fixture
def htmx_headers():
    return {"HTTP_HX_REQUEST": "true"}
```

## Verifying Query Counts & HTMX Contracts

```python
def test_list_avoids_n_plus_one(auth_client, django_assert_num_queries):
    with django_assert_num_queries(2):
        response = auth_client.get(reverse("items:list"))
    assert response.status_code == 200


def test_htmx_partial_varies_on_header(auth_client, htmx_headers):
    response = auth_client.get(reverse("items:list"), **htmx_headers)
    assert response.status_code == 200
    assert "HX-Request" in response.headers.get("Vary", "")
```

## Manual Code Review Checklist

- [ ] No business logic in views; model vs service boundary respected.
- [ ] All detail/mutation endpoints scope queries via `.visible_to(request.user)`.
- [ ] `select_related()` / `prefetch_related()` applied to eliminate N+1 queries.
- [ ] HTMX invalid form submissions re-render the partial with HTTP 200.
- [ ] Views varying on `request.htmx` use `@vary_on_headers("HX-Request")`.
- [ ] No secrets, hardcoded URLs, or `os.getenv` in `apps/`.
- [ ] User-facing strings wrapped for i18n (`gettext` / `{% translate %}`).
- [ ] Background tasks (Huey) receive primitive IDs and are idempotent.
