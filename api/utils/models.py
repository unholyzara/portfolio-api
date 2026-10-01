import uuid

from django.db import models
from django.core.validators import RegexValidator


class UUIDModel(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )

    class Meta:
        abstract = True


class ActiveModel(models.Model):
    active = models.BooleanField(default=False)

    class Meta:
        abstract = True


date_validator = RegexValidator(
    regex=r"^(0[1-9]|1[0-2])/\d{4}$|^(0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])/\d{4}$",
    message="Use MM/YYYY or DD/MM/YYYY.",
)
