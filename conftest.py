import pytest
from django.contrib.auth import get_user_model

from apps.users.tests.factories import UserFactory

User = get_user_model()


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def admin_user() -> User:
    return UserFactory(is_admin=True)
