from rest_framework import serializers

from .models import Overview, PersonalInfo, SpokenLanguage


class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = ["uuid", "name", "surname", "birth_date"]


class OverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overview
        fields = ["uuid", "active", "text"]


class SpokenLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpokenLanguage
        fields = ["uuid", "active", "name", "level"]
