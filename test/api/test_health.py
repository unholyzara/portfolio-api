import pytest
from django.core.cache import cache
from django.urls import reverse

from site_settings.models import SiteSettings


@pytest.mark.django_db
class TestHealthView:
    url = reverse("api-health")

    def test_health(self, api_client):
        r = api_client.get(self.url)
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}

    def test_health_during_maintenance(self, api_client):
        SiteSettings.objects.update(maintenance=True)
        cache.clear()
        r = api_client.get(self.url)
        assert r.status_code == 200
