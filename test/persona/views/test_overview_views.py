import copy

from uuid import UUID, uuid4

import pytest

from django.urls import reverse
from rest_framework.test import APIClient

from persona.models import Overview

PAYLOAD = {
    "active": True,
    "text": "overview text",
}


@pytest.mark.django_db
class TestOverview:
    def setup_method(self):
        self.list_url = reverse("overview-list")

    def _get_detail_url(self, uuid: UUID):
        return reverse("overview-detail", kwargs={"uuid": uuid})

    def _create_overview(self, **overrides):
        values = copy.deepcopy(PAYLOAD)
        values.update(overrides)
        return Overview.objects.create(**values)

    def test_list(self, staff_client):
        active_obj = self._create_overview()
        not_active_obj = self._create_overview(
            active=False, text="not active-text"
        )
        r = staff_client.get(self.list_url, PAYLOAD, format="json")
        assert r.status_code == 200
        assert [overview["text"] for overview in r.json()] == [
            active_obj.text,
            not_active_obj.text,
        ]

    def test_list_no_staff(self):
        active_obj = self._create_overview()
        self._create_overview(active=False, text="not active-text")
        r = APIClient().get(self.list_url, PAYLOAD, format="json")
        assert r.status_code == 200
        assert [overview["text"] for overview in r.json()] == [active_obj.text]

    def test_retrieve(self, staff_client):
        obj = self._create_overview()
        url = self._get_detail_url(uuid=obj.uuid)
        r = staff_client.get(url)
        assert r.json()["text"] == obj.text

    def test_retrieve_404(self, staff_client):
        test_uuid = uuid4()
        url = self._get_detail_url(uuid=test_uuid)
        r = staff_client.get(url)
        assert r.status_code == 404

    def test_retrieve_no_staff(self):
        obj = self._create_overview()
        url = self._get_detail_url(uuid=obj.uuid)
        r = APIClient().get(url)
        assert r.json()["text"] == obj.text

    def test_retrieve_no_staff_not_active(self):
        obj = self._create_overview(active=False)
        url = self._get_detail_url(uuid=obj.uuid)
        r = APIClient().get(url)
        assert r.status_code == 404

    def test_create(self, staff_client):
        r = staff_client.post(self.list_url, PAYLOAD, format="json")
        assert r.status_code == 201
        assert Overview.objects.get().text == PAYLOAD["text"]

    def test_create_no_staff(self):
        r = APIClient().post(self.list_url, PAYLOAD, format="json")
        assert r.status_code == 403
        assert not Overview.objects.exists()

    def test_update(self, staff_client):
        obj = self._create_overview()
        new_text = "new-text"
        url = self._get_detail_url(uuid=obj.uuid)
        r = staff_client.put(url, {**PAYLOAD, "text": new_text}, format="json")
        assert r.status_code == 200
        assert Overview.objects.get().text == new_text

    def test_partial_update(self, staff_client):
        obj = self._create_overview()
        new_text = "new-text"
        url = self._get_detail_url(uuid=obj.uuid)
        r = staff_client.patch(url, {"text": new_text}, format="json")
        assert r.status_code == 200
        assert Overview.objects.get().text == new_text

    def test_update_404(self, staff_client):
        test_uuid = uuid4()
        url = self._get_detail_url(uuid=test_uuid)
        r = staff_client.put(url, PAYLOAD, format="json")
        assert r.status_code == 404
        assert not Overview.objects.exists()

    def test_update_not_staff(self):
        obj = self._create_overview()
        new_text = "new-text"
        url = self._get_detail_url(uuid=obj.uuid)
        r = APIClient().put(url, {**PAYLOAD, "text": new_text}, format="json")
        assert r.status_code == 403
        assert Overview.objects.get().text == obj.text

    def test_partial_update_no_staff(self):
        obj = self._create_overview()
        new_text = "new-text"
        url = self._get_detail_url(uuid=obj.uuid)
        r = APIClient().patch(url, {"text": new_text}, format="json")
        assert r.status_code == 403
        assert Overview.objects.get().text == obj.text

    def test_destroy(self, staff_client):
        obj = self._create_overview()
        url = self._get_detail_url(uuid=obj.uuid)
        r = staff_client.delete(url, format="json")
        assert r.status_code == 204
        assert not Overview.objects.exists()

    def test_destroy_404(self, staff_client):
        obj = self._create_overview()
        test_uuid = uuid4()
        url = self._get_detail_url(uuid=test_uuid)
        r = staff_client.delete(url, format="json")
        assert r.status_code == 404
        assert Overview.objects.get().text == obj.text

    def test_destroy_not_staff(self):
        obj = self._create_overview()
        url = self._get_detail_url(uuid=obj.uuid)
        r = APIClient().put(url, format="json")
        assert r.status_code == 403
        assert Overview.objects.exists()
