from collections.abc import Iterable
from typing import Any

from django.db import models
from django.db import transaction

from api.utils import models as models_utils


class PersonalInfo(models_utils.UUIDModel):
    name = models.CharField()
    surname = models.CharField()
    birth_date = models.DateField()
    job_role = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField()

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


class SpokenLanguage(
    models_utils.UUIDModel, models_utils.ActiveModel, models_utils.LevelModel
):
    name = models.CharField()

    class Meta:
        indexes = [
            models.Index(
                fields=["active", "name"],
                name="spokenlanguage_active_name_idx",
                condition=models.Q(active=True),
            ),
        ]


class Education(models_utils.UUIDModel, models_utils.ActiveModel):
    institution = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-end_date", "-start_date"]
