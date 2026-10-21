import copy

from uuid import UUID, uuid4

import pytest

from django.urls import reverse
from rest_framework.test import APIClient

from persona.models import SpokenLanguage
from persona.utils.enums import Levels

PAYLOAD = {
    "active": True,
    "name": "name",
    "level": Levels.MD.name,
}


@pytest.mark.django_db
class TestSpokenLanguage:
    def setup_method(self):
        self.list_url = reverse("spokenlanguage-list")

    def _get_detail_url(self, uuid: UUID):
        return reverse("spokenlanguage-detail", kwargs={"uuid": uuid})

    def _create_spoken_language(self, **overrides):
        values = copy.deepcopy(PAYLOAD)
        values.update(overrides)
        return SpokenLanguage.objects.create(**values)

    def test_list(self, staff_client):
        active_obj = self._create_spoken_language()
        not_active_obj = self._create_spoken_language(
            active=False, name="name-2"
        )
        r = staff_client.get(self.list_url, PAYLOAD, format="json")
        assert r.status_code == 200
        assert [overview["name"] for overview in r.json()] == [
            active_obj.name,
            not_active_obj.name,
        ]

    def test_list_no_staff(self):
        active_obj = self._create_spoken_language()
        self._create_spoken_language(active=False, name="name-2")
        r = APIClient().get(self.list_url, PAYLOAD, format="json")
        assert r.status_code == 200
        assert [overview["name"] for overview in r.json()] == [active_obj.name]

    def test_retrieve(self, staff_client):
        obj = self._create_spoken_language()
        url = self._get_detail_url(uuid=obj.uuid)
        r = staff_client.get(url)
        assert r.json()["name"] == obj.name

    def test_retrieve_404(self, staff_client):
        test_uuid = uuid4()
        url = self._get_detail_url(uuid=test_uuid)
        r = staff_client.get(url)
        assert r.status_code == 404

    def test_retrieve_no_staff(self):
        obj = self._create_spoken_language()
        url = self._get_detail_url(uuid=obj.uuid)
        r = APIClient().get(url)
        assert r.json()["name"] == obj.name

    def test_retrieve_no_staff_not_active(self):
        obj = self._create_spoken_language(active=False)
        url = self._get_detail_url(uuid=obj.uuid)
        r = APIClient().get(url)
        assert r.status_code == 404

    def test_create(self, staff_client):
        r = staff_client.post(self.list_url, PAYLOAD, format="json")
        assert r.status_code == 201
        assert SpokenLanguage.objects.get().name == PAYLOAD["name"]

    def test_create_no_staff(self):
        r = APIClient().post(self.list_url, PAYLOAD, format="json")
        assert r.status_code == 403
        assert not SpokenLanguage.objects.exists()

    def test_update(self, staff_client):
        obj = self._create_spoken_language()
        new_name = "new-name"
        url = self._get_detail_url(uuid=obj.uuid)
        r = staff_client.put(url, {**PAYLOAD, "name": new_name}, format="json")
        assert r.status_code == 200
        assert SpokenLanguage.objects.get().name == new_name

    def test_partial_update(self, staff_client):
        obj = self._create_spoken_language()
        new_name = "new-name"
        url = self._get_detail_url(uuid=obj.uuid)
        r = staff_client.patch(url, {"name": new_name}, format="json")
        assert r.status_code == 200
        assert SpokenLanguage.objects.get().name == new_name

    def test_update_404(self, staff_client):
        test_uuid = uuid4()
        url = self._get_detail_url(uuid=test_uuid)
        r = staff_client.put(url, PAYLOAD, format="json")
        assert r.status_code == 404
        assert not SpokenLanguage.objects.exists()

    def test_update_not_staff(self):
        obj = self._create_spoken_language()
        new_name = "new-name"
        url = self._get_detail_url(uuid=obj.uuid)
        r = APIClient().put(url, {**PAYLOAD, "name": new_name}, format="json")
        assert r.status_code == 403
        assert SpokenLanguage.objects.get().name == obj.name

    def test_partial_update_no_staff(self):
        obj = self._create_spoken_language()
        new_name = "new-name"
        url = self._get_detail_url(uuid=obj.uuid)
        r = APIClient().patch(url, {"name": new_name}, format="json")
        assert r.status_code == 403
        assert SpokenLanguage.objects.get().name == obj.name

    def test_destroy(self, staff_client):
        obj = self._create_spoken_language()
        url = self._get_detail_url(uuid=obj.uuid)
        r = staff_client.delete(url, format="json")
        assert r.status_code == 204
        assert not SpokenLanguage.objects.exists()

    def test_destroy_404(self, staff_client):
        obj = self._create_spoken_language()
        test_uuid = uuid4()
        url = self._get_detail_url(uuid=test_uuid)
        r = staff_client.delete(url, format="json")
        assert r.status_code == 404
        assert SpokenLanguage.objects.get().name == obj.name

    def test_destroy_not_staff(self):
        obj = self._create_spoken_language()
        url = self._get_detail_url(uuid=obj.uuid)
        r = APIClient().put(url, format="json")
        assert r.status_code == 403
        assert SpokenLanguage.objects.exists()
