from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.text import Truncator
from modeltranslation.admin import TabbedTranslationAdmin, TranslationAdmin

from .models import Overview, PersonalInfo, SpokenLanguage, Education


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ("name", "surname", "birth_date")

    def has_add_permission(self, request: HttpRequest) -> bool:
        return not PersonalInfo.objects.exists()


@admin.register(Overview)
class OverviewAdmin(TabbedTranslationAdmin):
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
class SpokenLanguageAdmin(TranslationAdmin):
    list_display = ("name", "level", "active")
    list_filter = ("active", "level")
    search_fields = ("name_it", "name_en")
    ordering = ("name",)


@admin.register(Education)
class EducationAdmin(TabbedTranslationAdmin):
    list_display = ("qualification", "field_of_study", "active")
    list_filter = ("active",)
    search_fields = (
        "qualification_it",
        "qualification_en",
        "field_of_study_it",
        "field_of_study_en",
    )
    ordering = ("qualification", "field_of_study")
