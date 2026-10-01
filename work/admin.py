from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Company, TechnicalSkill, SoftSkill, WorkExperience


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(TechnicalSkill)
class TechnicalSkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

    @admin.action(description="Set selected technical skills as active")
    def set_active(
        self, request: HttpRequest, queryset: QuerySet[TechnicalSkill]
    ) -> None:
        skill = queryset.get()
        skill.active = True
        skill.save()
        self.message_user(request, "Skills set as active.")


@admin.register(SoftSkill)
class SoftSkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

    @admin.action(description="Set selected technical skills as active")
    def set_active(
        self, request: HttpRequest, queryset: QuerySet[SoftSkill]
    ) -> None:
        skill = queryset.get()
        skill.active = True
        skill.save()
        self.message_user(request, "Skills set as active.")


@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "company",
        "active",
    ]
    list_filter = [
        "active",
        "technical_skills",
        "soft_skills",
    ]
    search_fields = [
        "title",
        "description",
        "company__name",
        "technical_skills__name",
        "soft_skills__name",
    ]
    ordering = [
        "-start_date",
    ]
