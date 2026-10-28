from rest_framework import serializers
from modeltranslation.utils import get_translation_fields

from .models import SiteSettings


class SiteSettingsStaffReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = [
            "uuid",
            "maintenance",
            *get_translation_fields("maintenance_message"),
        ]


class SiteSettingsStaffWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = [
            "maintenance",
            *get_translation_fields("maintenance_message"),
        ]
