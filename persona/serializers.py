from rest_framework import serializers
from modeltranslation.utils import get_translation_fields

from .models import Overview, PersonalInfo, SpokenLanguage, Education
from .exceptions import PersonalInfoAlreadyExists


class PersonalInfoReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = [
            "uuid",
            "name",
            "surname",
            "birth_date",
            "job_role",
            "email",
            "phone_number",
        ]


class PersonalInfoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = [
            "name",
            "surname",
            "birth_date",
            "job_role",
            "email",
            "phone_number",
        ]

    def validate(self, attrs):
        if self.instance is None and PersonalInfo.objects.exists():
            raise PersonalInfoAlreadyExists()
        return attrs


class OverviewReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overview
        fields = ["uuid", "text"]


class OverviewStaffReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overview
        fields = ["uuid", "active", *get_translation_fields("text")]


class OverviewWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overview
        fields = ["active", *get_translation_fields("text")]
        extra_kwargs = {
            "text_it": {
                "required": True,
                "allow_null": False,
                "allow_blank": False,
            },
        }


class SpokenLanguageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpokenLanguage
        fields = ["uuid", "name", "level"]


class SpokenLanguageStaffReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpokenLanguage
        fields = ["uuid", "active", *get_translation_fields("name"), "level"]


class SpokenLanguageWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpokenLanguage
        fields = ["active", *get_translation_fields("name"), "level"]
        extra_kwargs = {
            "name_it": {
                "required": True,
                "allow_null": False,
                "allow_blank": False,
            },
        }


class EducationReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            "uuid",
            "institution",
            "qualification",
            "field_of_study",
            "start_date",
            "end_date",
            "description",
        ]


class EducationStaffReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            "uuid",
            "active",
            "institution",
            *get_translation_fields("qualification"),
            *get_translation_fields("field_of_study"),
            "start_date",
            "end_date",
            *get_translation_fields("description"),
        ]


class EducationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            "active",
            "institution",
            *get_translation_fields("qualification"),
            *get_translation_fields("field_of_study"),
            "start_date",
            "end_date",
            *get_translation_fields("description"),
        ]
        extra_kwargs = {
            "qualification_it": {
                "required": True,
                "allow_null": False,
                "allow_blank": False,
            },
        }
