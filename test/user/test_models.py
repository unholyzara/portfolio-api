import pytest
from django.contrib.auth import authenticate
from django.db import IntegrityError, transaction

from user.models import User


@pytest.mark.django_db
class TestUserEmail:
    @pytest.mark.parametrize(
        "raw", [" Staff@Example.COM ", "STAFF@example.com"]
    )
    def test_create_user_normalizes_email(self, make_user, email, raw):
        assert make_user(email=raw).email == email

    def test_save_normalizes_email(self, email):
        user = User(email="Staff@Example.COM")
        user.save()
        assert user.email == email

    def test_authenticate_is_case_insensitive(self, make_user, password):
        make_user()
        assert (
            authenticate(email="STAFF@Example.com", password=password)
            is not None
        )

    def test_database_rejects_case_variants(self, make_user):
        make_user()
        other = make_user(email="other@example.com")
        with pytest.raises(IntegrityError), transaction.atomic():
            User.objects.filter(pk=other.pk).update(email="STAFF@example.com")
