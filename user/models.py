from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Lower
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    username = None  # type: ignore
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("email"), name="user_email_lower_unique"
            ),
        ]
        ordering = ["email"]

    def save(self, *args, **kwargs):
        self.email = type(self).objects.normalize_email(self.email)
        super().save(*args, **kwargs)
