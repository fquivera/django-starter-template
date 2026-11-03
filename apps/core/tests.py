import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_home_page_status_code(client):
    """Verifies that the home page renders with status 200."""
    url = reverse("core:home")
    response = client.get(url)
    assert response.status_code == 200
    assert "Django" in response.content.decode()


@pytest.mark.django_db
def test_health_check_endpoint(client):
    """Verifies that health check endpoint returns 200 and json status ok."""
    url = reverse("core:health-check")
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.django_db
def test_htmx_counter_increment(client):
    """Verifies that HTMX counter increment updates session and returns partial."""
    url = reverse("core:counter-increment")
    response = client.post(url, HTTP_HX_REQUEST="true")
    assert response.status_code == 200
    assert "toast-container" in response.content.decode()
    assert client.session["counter"] == 1
