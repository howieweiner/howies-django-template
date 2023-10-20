import pytest
from django.urls import reverse

from apps.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_login_required_to_access_manage_view(client):
    url = reverse("users:user-list")

    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith("/login/")


def test_user_without_admin_cannot_access_manage_view(client, user):
    url = reverse("users:user-list")

    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 302


def test_admin_user_can_access_manage_view(client, admin_user):
    url = reverse("users:user-list")

    client.force_login(admin_user)
    response = client.get(url)
    assert response.status_code == 200


def test_admin_user_cannot_remove_admin_role_from_self(client, admin_user):
    url = reverse("users:user-update", args=[admin_user.id])

    client.force_login(admin_user)
    client.post(
        url,
        {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@user.com",
            "is_admin": False,
        },
    )

    # as the field is disabled, the value is ignored by the form. Therefore, the update succeeds
    # without the admin role being removed. There will be no form validation error.
    admin_user.refresh_from_db()
    assert admin_user.is_admin is True


def test_admin_user_cannot_deactivate_self(client, admin_user):
    url = reverse("users:user-update", args=[admin_user.id])

    client.force_login(admin_user)
    client.post(
        url,
        {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@user.com",
            "is_active": False,
        },
    )

    # as the field is disabled, the value is ignored by the form. Therefore, the update succeeds
    # without the admin role being removed. There will be no form validation error.
    admin_user.refresh_from_db()
    assert admin_user.is_active is True


def test_admin_user_can_remove_admin_role_from_another_user(client, admin_user):
    another_admin_user = UserFactory(is_admin=True)
    url = reverse("users:user-update", args=[another_admin_user.id])

    client.force_login(admin_user)
    client.post(
        url,
        {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@user.com",
            "is_admin": False,
        },
    )

    another_admin_user.refresh_from_db()
    assert another_admin_user.is_admin is False


def test_admin_user_can_deactivate_another_user(client, admin_user):
    another_admin_user = UserFactory(is_admin=True)
    url = reverse("users:user-update", args=[another_admin_user.id])

    client.force_login(admin_user)
    client.post(
        url,
        {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@user.com",
            "is_active": False,
        },
    )

    another_admin_user.refresh_from_db()
    assert another_admin_user.is_active is False


def test_admin_user_cannot_delete_own_account(client, admin_user):
    url = reverse("users:user-delete", args=[admin_user.id])

    client.force_login(admin_user)
    response = client.post(url)

    assert response.status_code == 403
