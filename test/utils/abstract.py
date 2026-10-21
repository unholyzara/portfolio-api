import abc, copy

from typing import Any, TypeVar
from uuid import uuid4

from django.urls import reverse
from rest_framework.test import APIClient

from api.utils.models import UUIDModel

UUIDModelType = TypeVar("UUIDModelType", bound=UUIDModel)


class AbstractModelViewsTest(abc.ABC):
    model: type[UUIDModelType]
    list_url_name: str
    retrieve_url_name: str
    payload: dict[str, Any]
    update_key: str
    update_value: str

    pk_key: str = "uuid"

    def setup_method(self):
        self.list_url = reverse(self.list_url_name)

    def _get_detail_url(self, pk_value: Any):
        return reverse(self.retrieve_url_name, kwargs={self.pk_key: pk_value})

    def create_object(self, **overrides):
        values = copy.deepcopy(self.payload)
        values.update(overrides)
        return self.model.objects.create(**values)

    def test_list(self, staff_client):
        first_obj = self.create_object()
        second_obj = self.create_object(**{self.update_key: self.update_value})
        r = staff_client.get(self.list_url)
        assert r.status_code == 200
        assert [obj[self.pk_key] for obj in r.json()] == [
            str(first_obj.uuid),
            str(second_obj.uuid),
        ]

    def test_retrieve(self, staff_client):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = staff_client.get(url)
        assert r.json()[self.pk_key] == str(obj.uuid)

    def test_retrieve_404(self, staff_client):
        test_uuid = uuid4()
        url = self._get_detail_url(pk_value=test_uuid)
        r = staff_client.get(url)
        assert r.status_code == 404

    def test_create(self, staff_client):
        r = staff_client.post(self.list_url, self.payload, format="json")
        assert r.status_code == 201
        created_obj = self.model.objects.get()
        dict_obj = created_obj.__dict__
        assert dict_obj[self.update_key] == self.payload[self.update_key]

    def test_create_no_staff(self):
        r = APIClient().post(self.list_url, self.payload, format="json")
        assert r.status_code == 403
        assert not self.model.objects.exists()

    def test_update(self, staff_client):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = staff_client.put(
            url,
            {**self.payload, self.update_key: self.update_value},
            format="json",
        )
        assert r.status_code == 200
        updated_obj = self.model.objects.get()
        dict_obj = updated_obj.__dict__
        assert dict_obj[self.update_key] == self.update_value

    def test_partial_update(self, staff_client):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = staff_client.patch(
            url, {self.update_key: self.update_value}, format="json"
        )
        assert r.status_code == 200
        updated_obj = self.model.objects.get()
        dict_obj = updated_obj.__dict__
        assert dict_obj[self.update_key] == self.update_value

    def test_update_404(self, staff_client):
        test_uuid = uuid4()
        url = self._get_detail_url(pk_value=test_uuid)
        r = staff_client.put(url, self.payload, format="json")
        assert r.status_code == 404
        assert not self.model.objects.exists()

    def test_update_not_staff(self):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = APIClient().put(
            url,
            {**self.payload, self.update_key: self.update_value},
            format="json",
        )
        assert r.status_code == 403
        updated_obj = self.model.objects.get()
        dict_updated_obj = updated_obj.__dict__
        dict_obj = obj.__dict__
        assert dict_updated_obj[self.update_key] == dict_obj[self.update_key]

    def test_partial_update_no_staff(self):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = APIClient().patch(
            url, {self.update_key: self.update_value}, format="json"
        )
        assert r.status_code == 403
        not_updated_obj = self.model.objects.get()
        dict_not_updated_obj = not_updated_obj.__dict__
        dict_obj = obj.__dict__
        assert (
            dict_not_updated_obj[self.update_key] == dict_obj[self.update_key]
        )

    def test_destroy(self, staff_client):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = staff_client.delete(url, format="json")
        assert r.status_code == 204
        assert not self.model.objects.exists()

    def test_destroy_404(self, staff_client):
        self.create_object()
        test_uuid = uuid4()
        url = self._get_detail_url(pk_value=test_uuid)
        r = staff_client.delete(url, format="json")
        assert r.status_code == 404
        assert self.model.objects.exists()

    def test_destroy_not_staff(self):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = APIClient().put(url, format="json")
        assert r.status_code == 403
        assert self.model.objects.exists()


class AbstractActiveModelViewsTest(AbstractModelViewsTest):
    def test_list(self, staff_client):
        active_obj = self.create_object()
        not_active_obj = self.create_object(
            active=False, **{self.update_key: self.update_value}
        )
        r = staff_client.get(self.list_url, self.payload, format="json")
        assert r.status_code == 200
        assert [overview[self.pk_key] for overview in r.json()] == [
            str(active_obj.uuid),
            str(not_active_obj.uuid),
        ]

    def test_list_no_staff(self):
        active_obj = self.create_object()
        self.create_object(active=False, **{self.update_key: self.update_value})
        r = APIClient().get(self.list_url, self.payload, format="json")
        assert r.status_code == 200
        assert [overview[self.pk_key] for overview in r.json()] == [
            str(active_obj.uuid)
        ]

    def test_retrieve_no_staff(self):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = APIClient().get(url)
        assert r.json()[self.pk_key] == str(obj.uuid)

    def test_retrieve_no_staff_not_active(self):
        obj = self.create_object(active=False)
        url = self._get_detail_url(pk_value=obj.uuid)
        r = APIClient().get(url)
        assert r.status_code == 404
