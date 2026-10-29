import abc, copy

import pytest
from typing import Any, TypeVar
from uuid import uuid4

from django.core.cache import cache
from django.urls import reverse
from rest_framework.test import APIClient

from api.utils.models import UUIDModel
from site_settings.models import SiteSettings

UUIDModelType = TypeVar("UUIDModelType", bound=UUIDModel)


class AbstractModelViewsBaseTest(abc.ABC):
    model: type[UUIDModelType]
    list_url_name: str
    retrieve_url_name: str
    payload: dict[str, Any]
    staff_payload: dict[str, Any] | None = None
    update_key: str
    update_value: str

    pk_key: str = "uuid"

    def setup_method(self):
        self.list_url = reverse(self.list_url_name)

    @pytest.fixture(autouse=True)
    def _clear_cache(self):
        cache.clear()
        yield
        cache.clear()

    @pytest.fixture
    def maintenance_on(self):
        site_settings = SiteSettings.objects.get()
        site_settings.maintenance = True
        site_settings.save()

    @staticmethod
    def assert_maintenance(response):
        assert response.status_code == 503
        assert response.json() == {"detail": "maintenance"}

    def _get_detail_url(self, pk_value: Any):
        return reverse(self.retrieve_url_name, kwargs={self.pk_key: pk_value})

    def get_payload(self):
        return self.payload

    def create_object(self, **overrides):
        values = copy.deepcopy(self.get_payload())
        values.update(overrides)
        return self.model.objects.create(**values)


class AbstractModelViewsTest(AbstractModelViewsBaseTest):
    def test_list(self, api_client: APIClient):
        first_obj = self.create_object()
        second_obj = self.create_object(**{self.update_key: self.update_value})
        r = api_client.get(self.list_url)
        assert r.status_code == 200
        assert [obj[self.pk_key] for obj in r.json()] == [
            str(first_obj.uuid),
            str(second_obj.uuid),
        ]

    def test_list_maintenance(self, api_client: APIClient, maintenance_on):
        self.create_object()
        self.assert_maintenance(api_client.get(self.list_url))

    def test_retrieve(self, api_client: APIClient):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = api_client.get(url)
        assert r.json()[self.pk_key] == str(obj.uuid)

    def test_retrieve_404(self, api_client: APIClient):
        test_uuid = uuid4()
        url = self._get_detail_url(pk_value=test_uuid)
        r = api_client.get(url)
        assert r.status_code == 404

    def test_retrieve_maintenance(self, api_client: APIClient, maintenance_on):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        self.assert_maintenance(api_client.get(url))

    def test_retrieve_404_maintenance(
        self, api_client: APIClient, maintenance_on
    ):
        url = self._get_detail_url(pk_value=uuid4())
        self.assert_maintenance(api_client.get(url))

    def test_create(self, api_client: APIClient):
        r = api_client.post(self.list_url, self.get_payload(), format="json")
        assert r.status_code == 405
        assert not self.model.objects.exists()

    def test_create_maintenance(self, api_client: APIClient, maintenance_on):
        r = api_client.post(self.list_url, self.get_payload(), format="json")
        self.assert_maintenance(r)
        assert not self.model.objects.exists()

    def test_update(self, api_client: APIClient):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = api_client.put(
            url,
            {**self.get_payload(), self.update_key: self.update_value},
            format="json",
        )
        assert r.status_code == 405
        updated_obj = self.model.objects.get()
        dict_updated_obj = updated_obj.__dict__
        dict_obj = obj.__dict__
        assert dict_updated_obj[self.update_key] == dict_obj[self.update_key]

    def test_update_maintenance(self, api_client: APIClient, maintenance_on):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = api_client.put(
            url,
            {**self.get_payload(), self.update_key: self.update_value},
            format="json",
        )
        self.assert_maintenance(r)
        assert self.model.objects.get().__dict__[self.update_key] == (
            obj.__dict__[self.update_key]
        )

    def test_destroy(self, api_client: APIClient):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = api_client.put(url, format="json")
        assert r.status_code == 405
        assert self.model.objects.exists()

    def test_destroy_maintenance(self, api_client: APIClient, maintenance_on):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = api_client.delete(url, format="json")
        self.assert_maintenance(r)
        assert self.model.objects.exists()


class AbstractStaffModelViewsTest(AbstractModelViewsBaseTest):
    def test_list(self, staff_client: APIClient):
        first_obj = self.create_object()
        second_obj = self.create_object(**{self.update_key: self.update_value})
        r = staff_client.get(self.list_url)
        assert r.status_code == 200
        response_data = r.json()
        response_uuids = [obj[self.pk_key] for obj in response_data]
        response_uuids.sort()
        expected_uuids = [
            str(first_obj.uuid),
            str(second_obj.uuid),
        ]
        expected_uuids.sort()
        assert response_uuids == expected_uuids

    def test_retrieve(self, staff_client: APIClient):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = staff_client.get(url)
        assert r.json()[self.pk_key] == str(obj.uuid)

    def test_retrieve_404(self, staff_client: APIClient):
        test_uuid = uuid4()
        url = self._get_detail_url(pk_value=test_uuid)
        r = staff_client.get(url)
        assert r.status_code == 404

    def test_retrieve_no_staff(self, api_client: APIClient):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = api_client.get(url)
        assert r.status_code == 403

    def test_create(self, staff_client: APIClient):
        payload = self.get_payload()
        r = staff_client.post(self.list_url, payload, format="json")
        assert r.status_code == 201
        created_obj = self.model.objects.get()
        dict_obj = created_obj.__dict__
        assert dict_obj[self.update_key] == payload[self.update_key]

    def test_create_no_staff(self, api_client: APIClient):
        r = api_client.post(self.list_url, self.get_payload(), format="json")
        assert r.status_code == 403
        assert not self.model.objects.exists()

    def test_update(self, staff_client: APIClient):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = staff_client.put(
            url,
            {**self.get_payload(), self.update_key: self.update_value},
            format="json",
        )
        assert r.status_code == 200
        updated_obj = self.model.objects.get()
        dict_obj = updated_obj.__dict__
        assert dict_obj[self.update_key] == self.update_value

    def test_update_404(self, staff_client: APIClient):
        test_uuid = uuid4()
        url = self._get_detail_url(pk_value=test_uuid)
        r = staff_client.put(url, self.get_payload(), format="json")
        assert r.status_code == 404
        assert not self.model.objects.exists()

    def test_update_not_staff(self, api_client: APIClient):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = api_client.put(
            url,
            {**self.get_payload(), self.update_key: self.update_value},
            format="json",
        )
        assert r.status_code == 403
        updated_obj = self.model.objects.get()
        dict_updated_obj = updated_obj.__dict__
        dict_obj = obj.__dict__
        assert dict_updated_obj[self.update_key] == dict_obj[self.update_key]

    def test_destroy(self, staff_client: APIClient):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = staff_client.delete(url, format="json")
        assert r.status_code == 204
        assert not self.model.objects.exists()

    def test_destroy_404(self, staff_client: APIClient):
        self.create_object()
        test_uuid = uuid4()
        url = self._get_detail_url(pk_value=test_uuid)
        r = staff_client.delete(url, format="json")
        assert r.status_code == 404
        assert self.model.objects.exists()

    def test_destroy_not_staff(self, api_client: APIClient):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = api_client.put(url, format="json")
        assert r.status_code == 403
        assert self.model.objects.exists()


class AbstractActiveModelViewsTest(AbstractModelViewsTest):
    def test_list(self, api_client: APIClient):
        active_obj = self.create_object()
        self.create_object(active=False, **{self.update_key: self.update_value})
        r = api_client.get(self.list_url)
        assert r.status_code == 200
        assert [overview[self.pk_key] for overview in r.json()] == [
            str(active_obj.uuid),
        ]

    def test_retrieve_no_staff(self, api_client: APIClient):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = api_client.get(url)
        assert r.json()[self.pk_key] == str(obj.uuid)

    def test_retrieve_no_staff_not_active(self, api_client: APIClient):
        obj = self.create_object(active=False)
        url = self._get_detail_url(pk_value=obj.uuid)
        r = api_client.get(url)
        assert r.status_code == 404
