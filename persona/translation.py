from modeltranslation.translator import register, TranslationOptions

from .models import PersonalInfo, Overview, SpokenLanguage, Education


@register(PersonalInfo)
class PersonalInfoTranslationOptions(TranslationOptions):
    fields = (
        "job_role",
        "location",
    )


@register(Overview)
class OverviewTranslationOptions(TranslationOptions):
    fields = (
        "short_text",
        "text",
    )


@register(SpokenLanguage)
class SpokenLanguageTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Education)
class EducationTranslationOptions(TranslationOptions):
    fields = (
        "qualification",
        "field_of_study",
        "description",
    )
