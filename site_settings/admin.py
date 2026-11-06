from django.contrib import admin

from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("uuid", "maintenance")

    def has_delete_permission(self, request, obj=None):
        return False
