from django.db import models
from django.utils.translation import gettext_lazy as _

from api.utils import models as models_utils


class Company(models_utils.UUIDModel):
    name = models.CharField()
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class SkillType(models.TextChoices):
    TECHNICAL = "technical", "Technical"
    SOFT = "soft", "Soft"


class Skill(models_utils.UUIDModel, models_utils.ActiveModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    typology = models.CharField(max_length=20, choices=SkillType.choices)

    class Meta:
        ordering = ["typology", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["typology", "name_it"],
                name="unique_skill_typology_name_it",
            ),
        ]

    def __str__(self):
        return self.name


class TechnologyType(models.TextChoices):
    LANGUAGE = "language", _("Linguagio")
    FRAMEWORK = "framework", "Framework"
    LIBRARY = "library", _("Libreria")
    MARKUP = "markup", "Markup"
    STYLESHEET = "stylesheet", "Stylesheet"
    TOOL = "tool", "Tool"
    DATABASE = "database", "Database"


class Technology(
    models_utils.UUIDModel, models_utils.ActiveModel, models_utils.LevelModel
):
    name = models.CharField(max_length=100, unique=True)
    typology = models.CharField(max_length=20, choices=TechnologyType.choices)

    class Meta:
        ordering = ["typology", "name"]

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
        Skill,
        related_name="work_experiences_tech",
        limit_choices_to={"typology": SkillType.TECHNICAL},
        blank=True,
    )
    soft_skills = models.ManyToManyField(
        Skill,
        related_name="work_experiences_soft",
        limit_choices_to={"typology": SkillType.SOFT},
        blank=True,
    )
    technologies = models.ManyToManyField(
        Technology,
        related_name="work_experiences",
        blank=True,
    )

    def __str__(self):
        if self.company:
            return f"{self.title} - {self.company.name}"
        else:
            return self.title


class Project(models_utils.UUIDModel, models_utils.ActiveModel):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(
        blank=True,
        null=True,
    )
    technologies = models.ManyToManyField(
        Technology,
        related_name="projects",
        blank=True,
    )
    work_experience = models.ForeignKey(
        WorkExperience, blank=True, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class ProjectRepository(models_utils.UUIDModel):
    project = models.ForeignKey(
        Project, related_name="repositories", on_delete=models.CASCADE
    )
    url = models.URLField()
    label = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["label"]

    def __str__(self):
        return self.label or self.url
