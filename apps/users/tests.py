import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_custom_user_creation():
    """Verifies that the custom User model can be created and saved properly."""
    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="secretpassword123",
        organization="F&S Transport",
    )
    assert user.pk is not None
    assert user.organization == "F&S Transport"
    assert str(user) == "testuser"
