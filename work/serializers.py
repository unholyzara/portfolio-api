from rest_framework import serializers

from .models import (
    Company,
    TechnicalSkill,
    SoftSkill,
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


class TechnicalSkillReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalSkill
        fields = ["uuid", "name", "description"]


class TechnicalSkillStaffReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalSkill
        fields = ["uuid", "active", "name", "description"]


class TechnicalWriteSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalSkill
        fields = ["active", "name", "description"]


class SoftSkillReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftSkill
        fields = ["uuid", "name", "description"]


class SoftSkillStaffReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftSkill
        fields = ["uuid", "active", "name", "description"]


class SoftSkillWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftSkill
        fields = ["active", "name", "description"]


class TechnologyReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ["uuid", "name", "typology", "level"]


class TechnologyStaffReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ["uuid", "active", "name", "typology", "level"]


class TechnologyWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ["active", "name", "typology", "level"]


class WorkExperienceReadSerializer(serializers.ModelSerializer):
    company = CompanyReadSerializer(read_only=True)
    technical_skills = TechnicalSkillReadSerializer(many=True, read_only=True)
    soft_skills = SoftSkillReadSerializer(many=True, read_only=True)

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
    technical_skills = TechnicalSkillReadSerializer(many=True, read_only=True)
    soft_skills = SoftSkillReadSerializer(many=True, read_only=True)

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
        queryset=TechnicalSkill.objects.all(),
        many=True,
        required=False,
    )

    soft_skills = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=SoftSkill.objects.all(),
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
