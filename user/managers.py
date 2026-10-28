from typing import Any, TYPE_CHECKING

from django.contrib.auth.models import UserManager as DjangoUserManager

if TYPE_CHECKING:
    from django.contrib.auth.models import User


class UserManager(DjangoUserManager["User"]):
    use_in_migrations = True

    @classmethod
    def normalize_email(cls, email: str | None) -> str:
        return super().normalize_email(email).lower()

    def get_by_natural_key(self, username: str | None) -> "User":
        return super().get_by_natural_key(self.normalize_email(username))

    def _create_user(
        self,
        username: str | None,
        email: str | None,
        password: str | None,
        **extra_fields: Any,
    ) -> "User":
        if not email:
            raise ValueError("The email must be set")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        username: str | None = None,
        email: str | None = None,
        password: str | None = None,
        **extra_fields: Any,
    ) -> "User":
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(
        self,
        username: str | None = None,
        email: str | None = None,
        password: str | None = None,
        **extra_fields: Any,
    ) -> "User":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(username, email, password, **extra_fields)
