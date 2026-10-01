import uuid

from django.db import models


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
