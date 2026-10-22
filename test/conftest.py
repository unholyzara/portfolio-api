import pytest
from rest_framework.test import APIClient

from api.utils.types import ModelType


@pytest.fixture
def staff_client(db, django_user_model: type[ModelType]):
    user = django_user_model.objects.create_user(
        username="staff", password="x", is_staff=True
    )
    client = APIClient()
    client.force_authenticate(user)
    return client
