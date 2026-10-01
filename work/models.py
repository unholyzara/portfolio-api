from django.db import models

from api.utils import models as models_utils


class Company(models_utils.UUIDModel):
    name = models.CharField()
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class TechnicalSkill(models_utils.UUIDModel, models_utils.ActiveModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class SoftSkill(models_utils.UUIDModel, models_utils.ActiveModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class WorkExperience(models_utils.UUIDModel, models_utils.ActiveModel):
    title = models.CharField()
    description = models.TextField(
        blank=True,
        null=True,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        related_name="work_experiences",
    )
    start_date = models.CharField(
        max_length=10,
        validators=[models_utils.date_validator],
    )
    end_date = models.CharField(
        max_length=10,
        validators=[models_utils.date_validator],
        blank=True,
        null=True,
        default=None,
    )
    technical_skills = models.ManyToManyField(
        TechnicalSkill,
        related_name="work_experiences",
        blank=True,
    )
    soft_skills = models.ManyToManyField(
        SoftSkill,
        related_name="work_experiences",
        blank=True,
    )

    def __str__(self):
        if self.company:
            return f"{self.title} - {self.company.name}"
        else:
            return self.title
