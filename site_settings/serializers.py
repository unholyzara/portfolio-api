from rest_framework import serializers

from .models import SiteSettings


class SiteSettingsStaffReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = [
            "uuid",
            "maintenance",
        ]


class SiteSettingsStaffWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = [
            "maintenance",
        ]
