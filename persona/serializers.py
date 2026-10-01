from rest_framework import serializers

from .models import Overview, PersonalInfo, SpokenLanguage


class PersonalInfoReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = ["uuid", "name", "surname", "birth_date"]


class PersonalInfoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = ["name", "surname", "birth_date"]


class OverviewReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overview
        fields = ["uuid", "active", "text"]


class OverviewWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overview
        fields = ["active", "text"]


class SpokenLanguageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpokenLanguage
        fields = ["uuid", "active", "name", "level"]


class SpokenLanguageWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpokenLanguage
        fields = ["active", "name", "level"]
