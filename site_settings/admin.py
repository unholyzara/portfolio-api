from django.contrib import admin

from modeltranslation.admin import TabbedTranslationAdmin

from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(TabbedTranslationAdmin):
    list_display = ("maintenance", "maintenance_message")
