import pytest

from test.utils.abstract import (
    AbstractModelViewsTest,
    AbstractActiveModelViewsTest,
)

from work.models import Company, TechnicalSkill, SoftSkill


@pytest.mark.django_db
class TestCompany(AbstractModelViewsTest):
    model = Company
    list_url_name = "company-list"
    retrieve_url_name = "company-detail"
    payload = {
        "name": "company 1",
        "website": None,
    }
    update_key = "name"
    update_value = "company 2"


@pytest.mark.django_db
class TestTechnicalSkill(AbstractActiveModelViewsTest):
    model = TechnicalSkill
    list_url_name = "technicalskill-list"
    retrieve_url_name = "technicalskill-detail"
    payload = {
        "active": True,
        "name": "technicalskill 1",
        "description": "description",
    }
    update_key = "name"
    update_value = "technicalskill 2"


@pytest.mark.django_db
class TestSoftSkill(AbstractActiveModelViewsTest):
    model = SoftSkill
    list_url_name = "softskill-list"
    retrieve_url_name = "softskill-detail"
    payload = {
        "active": True,
        "name": "softskill 1",
        "description": "description",
    }
    update_key = "name"
    update_value = "softskill 2"
