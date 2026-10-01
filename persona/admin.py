from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.text import Truncator

from .models import Overview, PersonalInfo, SpokenLanguage


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ("name", "surname", "birth_date")

    def has_add_permission(self, request: HttpRequest) -> bool:
        return not PersonalInfo.objects.exists()


@admin.register(Overview)
class OverviewAdmin(admin.ModelAdmin):
    list_display = ("text_preview", "active")
    list_filter = ("active",)
    exclude = ("active",)
    actions = ("set_active",)

    @admin.display(description="text")
    def text_preview(self, obj: Overview) -> str:
        return Truncator(obj.text).chars(80)

    @admin.action(description="Set selected overview as active")
    def set_active(
        self, request: HttpRequest, queryset: QuerySet[Overview]
    ) -> None:
        if queryset.count() != 1:
            self.message_user(
                request, "Select exactly one overview.", messages.ERROR
            )
            return
        overview = queryset.get()
        overview.active = True
        overview.save()
        self.message_user(request, "Overview set as active.")


@admin.register(SpokenLanguage)
class SpokenLanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "active")
    list_filter = ("active", "level")
    search_fields = ("name",)
    ordering = ("name",)
