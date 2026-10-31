from rest_framework import serializers
from modeltranslation.utils import get_translation_fields

from .models import (
    Company,
    SkillType,
    Skill,
    Technology,
    WorkExperience,
    WorkResponsibility,
    Project,
    ProjectRepository,
)


class CompanyReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["uuid", "name", "website"]


class CompanyWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["name", "website"]


class SkillReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["uuid", "typology", "name", "description"]


class SkillStaffReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            "uuid",
            "active",
            "typology",
            *get_translation_fields("name"),
            *get_translation_fields("description"),
        ]


class SkillWriteSerializer(serializers.ModelSerializer):
    name_it = serializers.CharField(max_length=100)
    name_en = serializers.CharField(
        max_length=100, required=False, allow_null=True
    )

    class Meta:
        model = Skill
        fields = [
            "active",
            "typology",
            *get_translation_fields("name"),
            *get_translation_fields("description"),
        ]

    def validate(self, attrs):
        typology = attrs.get(
            "typology", getattr(self.instance, "typology", None)
        )
        errors = {}
        value = attrs.get("name_it", getattr(self.instance, "name_it", None))
        others = Skill.objects.filter(typology=typology, name_it=value)
        if self.instance:
            others = others.exclude(pk=self.instance.pk)
        if others.exists():
            errors["name_it"] = (
                "A skill with this name already exists for this typology."
            )
        if errors:
            raise serializers.ValidationError(errors)
        return attrs


class TechnologyReadSerializer(serializers.ModelSerializer):
    typology_display = serializers.CharField(
        source="get_typology_display", read_only=True
    )

    class Meta:
        model = Technology
        fields = ["uuid", "name", "typology_display", "level"]


class TechnologyStaffReadSerializer(serializers.ModelSerializer):
    typology_display = serializers.CharField(
        source="get_typology_display", read_only=True
    )

    class Meta:
        model = Technology
        fields = ["uuid", "active", "name", "typology_display", "level"]


class TechnologyWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ["active", "name", "typology", "level"]


class WorkExperienceReadSerializer(serializers.ModelSerializer):
    company = CompanyReadSerializer(read_only=True)
    technical_skills = SkillReadSerializer(many=True, read_only=True)
    soft_skills = SkillReadSerializer(many=True, read_only=True)
    technologies = TechnologyReadSerializer(many=True, read_only=True)

    class Meta:
        model = WorkExperience
        fields = [
            "uuid",
            "title",
            "description",
            "company",
            "start_date",
            "end_date",
            "technical_skills",
            "soft_skills",
            "technologies",
        ]


class WorkExperienceStaffReadSerializer(serializers.ModelSerializer):
    company = CompanyReadSerializer(read_only=True)
    technical_skills = SkillStaffReadSerializer(many=True, read_only=True)
    soft_skills = SkillStaffReadSerializer(many=True, read_only=True)
    technologies = TechnologyStaffReadSerializer(many=True, read_only=True)

    class Meta:
        model = WorkExperience
        fields = [
            "uuid",
            "active",
            *get_translation_fields("title"),
            *get_translation_fields("description"),
            "company",
            "start_date",
            "end_date",
            "technical_skills",
            "soft_skills",
            "technologies",
        ]


class WorkExperienceWriteSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=Company.objects.all(),
        allow_null=True,
        required=False,
    )

    technical_skills = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=Skill.objects.filter(typology=SkillType.TECHNICAL),
        many=True,
        required=False,
    )

    soft_skills = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=Skill.objects.filter(typology=SkillType.SOFT),
        many=True,
        required=False,
    )

    technologies = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=Technology.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = WorkExperience
        fields = [
            "active",
            *get_translation_fields("title"),
            *get_translation_fields("description"),
            "company",
            "start_date",
            "end_date",
            "technical_skills",
            "soft_skills",
            "technologies",
        ]
        extra_kwargs = {
            "title_it": {
                "required": True,
                "allow_null": False,
                "allow_blank": False,
            },
        }


class WorkResponsibilityReadSerializer(serializers.ModelSerializer):
    work_experience = WorkExperienceReadSerializer(read_only=True)

    class Meta:
        model = WorkResponsibility
        fields = [
            "uuid",
            "work_experience",
            *get_translation_fields("description"),
            "order",
        ]


class WorkResponsibilityStaffReadSerializer(serializers.ModelSerializer):
    work_experience = WorkExperienceStaffReadSerializer(read_only=True)

    class Meta:
        model = WorkResponsibility
        fields = [
            "uuid",
            "active",
            "work_experience",
            "description",
            "order",
        ]


class WorkResponsibilityWriteSerializer(serializers.ModelSerializer):
    work_experience = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=WorkExperience.objects.all(),
        required=True,
    )

    class Meta:
        model = WorkResponsibility
        fields = [
            "active",
            "work_experience",
            *get_translation_fields("description"),
            "order",
        ]
        extra_kwargs = {
            "description_it": {
                "required": True,
                "allow_null": False,
                "allow_blank": False,
            },
        }


class ProjectReadSerializer(serializers.ModelSerializer):
    technologies = TechnologyReadSerializer(many=True, read_only=True)
    work_experience = WorkExperienceReadSerializer(read_only=True)

    class Meta:
        model = Project
        fields = [
            "uuid",
            "title",
            "description",
            "technologies",
            "work_experience",
        ]


class ProjectStaffReadSerializer(serializers.ModelSerializer):
    technologies = TechnologyReadSerializer(many=True, read_only=True)
    work_experience = WorkExperienceReadSerializer(read_only=True)

    class Meta:
        model = Project
        fields = [
            "uuid",
            "active",
            *get_translation_fields("title"),
            *get_translation_fields("description"),
            "technologies",
            "work_experience",
        ]


class ProjectWriteSerializer(serializers.ModelSerializer):
    technologies = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=Technology.objects.all(),
        many=True,
        required=False,
    )
    work_experience = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=WorkExperience.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Project
        fields = [
            "active",
            *get_translation_fields("title"),
            *get_translation_fields("description"),
            "technologies",
            "work_experience",
        ]
        extra_kwargs = {
            "title_it": {
                "required": True,
                "allow_null": False,
                "allow_blank": False,
            },
        }


class ProjectRepositoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRepository
        fields = [
            "uuid",
            "project",
            "url",
            "label",
        ]


class ProjectRepositoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRepository
        fields = [
            "project",
            "url",
            "label",
        ]
