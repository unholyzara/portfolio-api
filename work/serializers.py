from rest_framework import serializers

from .models import (
    Company,
    SkillType,
    Skill,
    Technology,
    WorkExperience,
    Project,
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
        fields = ["uuid", "active", "typology", "name", "description"]


class SkillWriteSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["active", "typology", "name", "description"]


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
        ]


class WorkExperienceStaffReadSerializer(serializers.ModelSerializer):
    company = CompanyReadSerializer(read_only=True)
    technical_skills = SkillStaffReadSerializer(many=True, read_only=True)
    soft_skills = SkillStaffReadSerializer(many=True, read_only=True)

    class Meta:
        model = WorkExperience
        fields = [
            "uuid",
            "active",
            "title",
            "description",
            "company",
            "start_date",
            "end_date",
            "technical_skills",
            "soft_skills",
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
            "title",
            "description",
            "company",
            "start_date",
            "end_date",
            "technical_skills",
            "soft_skills",
            "technologies",
        ]


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
            "title",
            "description",
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
            "title",
            "description",
            "technologies",
            "work_experience",
        ]
