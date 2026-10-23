from datetime import date

import pytest

from django.urls import reverse
from rest_framework.test import APIClient

from test.utils.abstract import (
    AbstractActiveModelViewsTest,
    AbstractStaffModelViewsTest,
)

from persona.models import PersonalInfo, Overview, SpokenLanguage

PAYLOAD = {
    "name": "Mario",
    "surname": "Rossi",
    "birth_date": "2000-01-01",
}


@pytest.mark.django_db
class TestPersonalInfoViews:
    def setup_method(self):
        self.url = reverse("personalinfo")

    def _create_personal_info(self, **overrides):
        values = {
            "name": "Mario",
            "surname": "Rossi",
            "birth_date": date(2000, 1, 1),
        }
        values.update(overrides)
        return PersonalInfo.objects.create(**values)

    def test_detail(self):
        obj = self._create_personal_info()
        r = APIClient().get(self.url)
        assert r.json()["name"] == obj.name

    def test_detail_404(self):
        r = APIClient().get(self.url)
        assert r.status_code == 404

    def test_create(self, staff_client):
        r = staff_client.post(self.url, PAYLOAD, format="json")
        assert r.status_code == 201
        assert PersonalInfo.objects.get().name == "Mario"

    def test_create_conflict(self, staff_client):
        self._create_personal_info()
        r = staff_client.post(
            self.url, {**PAYLOAD, "name": "Luigi"}, format="json"
        )
        assert r.status_code == 409
        assert PersonalInfo.objects.get().name == "Mario"

    def test_update(self, staff_client):
        self._create_personal_info()
        r = staff_client.put(
            self.url, {**PAYLOAD, "name": "Luigi"}, format="json"
        )
        assert r.status_code == 200
        assert PersonalInfo.objects.get().name == "Luigi"

    def test_update_404(self, staff_client):
        r = staff_client.put(self.url, PAYLOAD, format="json")
        assert r.status_code == 404
        assert not PersonalInfo.objects.exists()

    def test_destroy(self, staff_client):
        self._create_personal_info()
        r = staff_client.delete(self.url)
        assert r.status_code == 204
        assert not PersonalInfo.objects.exists()

    def test_destroy_404(self, staff_client):
        r = staff_client.delete(self.url)
        assert r.status_code == 404

    @pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
    def test_anonymous_cannot_write(self, method):
        self._create_personal_info()
        r = getattr(APIClient(), method)(self.url, PAYLOAD, format="json")
        assert r.status_code in (401, 403)
        assert PersonalInfo.objects.get().name == "Mario"


@pytest.mark.django_db
class TestOverviewViews(AbstractActiveModelViewsTest):
    model = Overview
    list_url_name = "overview-list"
    retrieve_url_name = "overview-detail"
    payload = {
        "active": True,
        "text": "overview text",
    }
    update_key = "text"
    update_value = "new-text"


@pytest.mark.django_db
class TestOverviewStaffViews(AbstractStaffModelViewsTest):
    model = Overview
    list_url_name = "overview-staff-list"
    retrieve_url_name = "overview-staff-detail"
    payload = {
        "active": True,
        "text_it": "overview text it",
    }
    update_key = "text_it"
    update_value = "new-text"


@pytest.mark.django_db
class TestSpokenLanguageViews(AbstractActiveModelViewsTest):
    model = SpokenLanguage
    list_url_name = "spoken-language-list"
    retrieve_url_name = "spoken-language-detail"
    payload = {
        "active": True,
        "name": "name",
        "level": 4,
    }
    update_key = "name"
    update_value = "new-name"


@pytest.mark.django_db
class TestSpokenLanguageStaffViews(AbstractStaffModelViewsTest):
    model = SpokenLanguage
    list_url_name = "spoken-language-staff-list"
    retrieve_url_name = "spoken-language-staff-detail"
    payload = {
        "active": True,
        "name_it": "name it",
        "level": 4,
    }
    update_key = "name_it"
    update_value = "new-name"
