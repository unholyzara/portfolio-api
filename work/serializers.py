from rest_framework import serializers

from .models import Company, TechnicalSkill, SoftSkill, WorkExperience


class CompanyReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["uuid", "name", "website"]


class CompanyWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["name", "website"]


class TechnicalReadSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalSkill
        fields = ["uuid", "name", "description"]


class TechnicalWriteSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalSkill
        fields = ["name", "description"]


class SoftSkillReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftSkill
        fields = ["uuid", "name", "description"]


class SoftSkillWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftSkill
        fields = ["name", "description"]


class WorkExperienceReadSerializer(serializers.ModelSerializer):
    company = CompanyReadSerializer(read_only=True)
    technical_skills = TechnicalReadSkillSerializer(many=True, read_only=True)
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

    class Meta:
        model = WorkExperience
        fields = [
            "title",
            "description",
            "company",
            "start_date",
            "end_date",
            "technical_skills",
            "soft_skills",
        ]
