from modeltranslation.translator import TranslationOptions, register

from .models import SiteSettings


@register(SiteSettings)
class SiteSettingsTranslationOptions(TranslationOptions):
    fields = ("maintenance_message",)
