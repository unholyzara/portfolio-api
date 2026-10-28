import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


@pytest.fixture
def email():
    return "staff@example.com"


@pytest.fixture
def password():
    return "S3cure-passw0rd!"


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def csrf_client():
    return APIClient(enforce_csrf_checks=True)


@pytest.fixture
def make_user(db, email, password):
    def factory(**extra):
        extra.setdefault("email", email)
        extra.setdefault("password", password)
        return get_user_model().objects.create_user(**extra)

    return factory


@pytest.fixture
def staff_user(make_user):
    return make_user(is_staff=True)


@pytest.fixture
def staff_client(make_user):
    user = make_user(is_staff=True)
    client = APIClient()
    client.force_authenticate(user)
    return client
