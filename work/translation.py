from modeltranslation.translator import register, TranslationOptions

from .models import Skill, WorkExperience, WorkResponsibility, Project


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


@register(WorkResponsibility)
class WorkResponsibilityTranslationOptions(TranslationOptions):
    fields = ("description",)


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "description",
    )
