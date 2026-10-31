from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from modeltranslation.admin import TabbedTranslationAdmin

from .models import (
    Company,
    Project,
    Skill,
    Technology,
    WorkExperience,
    WorkResponsibility,
    ProjectRepository,
)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Skill)
class SkillAdmin(TabbedTranslationAdmin):
    list_display = ("typology", "name", "active")
    list_filter = ("active", "typology")
    search_fields = ("name_it", "name_en")
    ordering = ("typology", "name")
    actions = ("set_active",)

    @admin.action(description="Set selected technical skills as active")
    def set_active(
        self, request: HttpRequest, queryset: QuerySet[Skill]
    ) -> None:
        updated = queryset.update(active=True)
        self.message_user(request, f"{updated} technical skills set as active.")


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "typology", "active")
    list_filter = ("active", "typology")
    search_fields = ("name",)
    ordering = ("typology", "name")


@admin.register(WorkExperience)
class WorkExperienceAdmin(TabbedTranslationAdmin):
    list_display = [
        "title",
        "company",
        "active",
    ]
    list_filter = [
        "active",
        "technical_skills",
        "soft_skills",
        "technologies",
    ]
    search_fields = [
        "title_it",
        "title_en",
        "description_it",
        "description_en",
        "company__name",
        "technical_skills__name_it",
        "technical_skills__name_en",
        "soft_skills__name_it",
        "soft_skills__name_en",
        "technologies__name",
    ]
    ordering = [
        "-start_date",
    ]


@admin.register(WorkResponsibility)
class WorkResponsibilityAdmin(TabbedTranslationAdmin):
    list_display = [
        "active",
        "work_experience",
        "description",
        "order",
    ]
    list_filter = [
        "active",
        "work_experience",
    ]
    search_fields = [
        "description_it",
        "description_en",
        "work_experience__title_it",
        "work_experience__title_en",
    ]


@admin.register(Project)
class ProjectAdmin(TabbedTranslationAdmin):
    list_display = ("title", "work_experience", "active")
    list_filter = ("active", "technologies")
    search_fields = (
        "title_it",
        "title_en",
        "description_it",
        "description_en",
        "technologies__name_it",
        "technologies__name_en",
    )
    ordering = ("title",)


@admin.register(ProjectRepository)
class ProjectRepositoryAdmin(admin.ModelAdmin):
    list_display = ("label", "project")
    list_filter = ("project",)
    search_fields = ("project__title",)
    ordering = ("label",)
