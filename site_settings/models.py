from django.core.cache import cache
from django.db import models

from api.utils import models as models_utils

CACHE_KEY = "site_settings_maintenance"


class SiteSettings(models_utils.UUIDModel):
    maintenance = models.BooleanField(default=False)
    maintenance_message = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                models.Value(1),
                name="sitesettings_singleton",
            ),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(CACHE_KEY)

    @classmethod
    def is_maintenance(cls):
        value = cache.get(CACHE_KEY)
        if value is None:
            value = bool(
                cls.objects.values_list("maintenance", flat=True).first()
            )
            cache.set(CACHE_KEY, value, 10)
        return value
