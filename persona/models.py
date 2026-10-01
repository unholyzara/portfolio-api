from collections.abc import Iterable
from typing import Any

from django.db import models
from django.db import transaction

from api.utils import models as models_utils

from .utils import enums


class PersonalInfo(models_utils.UUIDModel):
    name = models.CharField()
    surname = models.CharField()
    birth_date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                models.Value(1),
                name="personalinfo_singleton",
            ),
        ]


class Overview(models_utils.UUIDModel, models_utils.ActiveModel):
    text = models.TextField()

    def save(
        self,
        *args: Any,
        force_insert: bool = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        fields_to_update = (
            set(update_fields) if update_fields is not None else None
        )

        with transaction.atomic(using=using):
            if self.active and (
                fields_to_update is None or "active" in fields_to_update
            ):
                type(self).objects.select_for_update().filter(
                    active=True
                ).exclude(pk=self.pk).update(active=False)

            super().save(
                *args,
                force_insert=force_insert,
                force_update=force_update,
                using=using,
                update_fields=fields_to_update,
            )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["active"],
                condition=models.Q(active=True),
                name="overview_only_one_active",
            ),
        ]
        indexes = [
            models.Index(
                fields=["active"],
                name="overview_active_idx",
                condition=models.Q(active=True),
            ),
        ]


class SpokenLanguage(models_utils.UUIDModel, models_utils.ActiveModel):
    name = models.CharField()
    level = models.CharField(
        choices=enums.Levels.choices(), blank=True, null=True, max_length=2
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["active", "name"],
                name="spokenlanguage_active_name_idx",
                condition=models.Q(active=True),
            ),
        ]
