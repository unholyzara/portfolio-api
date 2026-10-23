from modeltranslation.translator import register, TranslationOptions

from .models import (
    TechnicalSkill,
    SoftSkill,
    WorkExperience,
    Project,
)


@register(TechnicalSkill)
class TechnicalSkillTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "description",
    )


@register(SoftSkill)
class SoftSkillTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "description",
    )


@register(WorkExperience)
class WorkExperienceTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "description",
    )


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "description",
    )
