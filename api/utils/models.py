import uuid

from django.db import models
from django.core.validators import (
    RegexValidator,
    MaxValueValidator,
    MinValueValidator,
)


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


class LevelModel(models.Model):
    level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )

    class Meta:
        abstract = True
        constraints = [
            models.CheckConstraint(
                condition=models.Q(level__gte=1, level__lte=5),
                name="programming_language_level_between_1_and_5",
            )
        ]


date_validator = RegexValidator(
    regex=r"^(0[1-9]|1[0-2])/\d{4}$|^(0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])/\d{4}$",
    message="Use MM/YYYY or DD/MM/YYYY.",
)
