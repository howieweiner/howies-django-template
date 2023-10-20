import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_login_required_to_access_dashboard_view(client):
    url = reverse("dashboard:home")

    response = client.get(url)
    assert response.status_code == 302
    assert "login" in response.url
