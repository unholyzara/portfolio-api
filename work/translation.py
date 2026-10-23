from modeltranslation.translator import register, TranslationOptions

from .models import Skill, WorkExperience, Project


@register(Skill)
class SkillTranslationOptions(TranslationOptions):
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
