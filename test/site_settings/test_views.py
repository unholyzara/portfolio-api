import pytest

from uuid import uuid4

from test.utils.abstract import AbstractStaffModelViewsTest

from site_settings.models import SiteSettings
from site_settings.serializers import SiteSettingsStaffReadSerializer


@pytest.mark.django_db
class TestSiteSettingsStaffViews(AbstractStaffModelViewsTest):
    model = SiteSettings
    list_url_name = "site-settings-staff-list"
    retrieve_url_name = "site-settings-staff-detail"
    update_key = "maintenance_message_it"
    update_value = "maintenance_message 2"

    def get_payload(self):
        obj = SiteSettings.objects.get()
        serialized_obj = SiteSettingsStaffReadSerializer(obj)
        data = dict(serialized_obj.data)
        data.pop("uuid")
        return data

    def create_object(self, **overrides):
        return SiteSettings.objects.get()

    def test_list(self, staff_client):
        r = staff_client.get(self.list_url)
        assert r.status_code == 200
        obj = SiteSettings.objects.get()
        response_data = r.json()
        response_uuids = [obj[self.pk_key] for obj in response_data]
        expected_uuids = [
            str(obj.uuid),
        ]
        expected_uuids.sort()
        assert response_uuids == expected_uuids

    def test_create(self, staff_client):
        payload = {**self.get_payload(), self.update_key: self.update_value}
        r = staff_client.post(self.list_url, payload, format="json")
        assert r.status_code == 405
        assert SiteSettings.objects.count() == 1

    def test_create_no_staff(self, api_client):
        assert SiteSettings.objects.count() == 1
        r = api_client.post(self.list_url, self.get_payload(), format="json")
        assert r.status_code == 403
        assert SiteSettings.objects.count() == 1

    def test_update_404(self, staff_client):
        assert SiteSettings.objects.count() == 1
        test_uuid = uuid4()
        url = self._get_detail_url(pk_value=test_uuid)
        r = staff_client.put(url, self.get_payload(), format="json")
        assert r.status_code == 404
        assert SiteSettings.objects.count() == 1

    def test_destroy(self, staff_client):
        obj = SiteSettings.objects.get()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = staff_client.delete(url, format="json")
        assert r.status_code == 405
        assert self.model.objects.exists()

    def test_destroy_404(self, staff_client):
        test_uuid = uuid4()
        url = self._get_detail_url(pk_value=test_uuid)
        r = staff_client.delete(url, format="json")
        assert r.status_code == 405
        assert SiteSettings.objects.count() == 1
