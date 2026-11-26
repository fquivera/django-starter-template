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


@pytest.mark.django_db
def test_modal_shell_uses_daisyui5_dialog(client):
    """Verifies the modal shell uses a native DaisyUI 5 dialog structure."""
    response = client.get(reverse("core:home"))
    html = response.content.decode()
    assert response.status_code == 200
    assert "<dialog" in html
    assert 'class="modal"' in html
    assert 'class="modal-box' in html
    assert 'class="modal-backdrop"' in html


@pytest.mark.django_db
def test_htmx_modal_demo_returns_partial(client):
    """Verifies the HTMX modal demo endpoint returns the modal partial."""
    response = client.get(reverse("core:modal-demo"), HTTP_HX_REQUEST="true")
    assert response.status_code == 200
    assert "close-modal" in response.content.decode()
