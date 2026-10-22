import pytest
from django.test import Client

from api.utils.types import ModelType


@pytest.fixture
def staff_client(db, django_user_model: type[ModelType]):
    user = django_user_model.objects.create_user(
        username="staff", password="x", is_staff=True
    )
    client = Client()
    client.force_login(user)
    return client
