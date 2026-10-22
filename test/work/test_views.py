import copy

import pytest

from rest_framework.test import APIClient

from test.utils.abstract import (
    AbstractModelViewsTest,
    AbstractActiveModelViewsTest,
)

from work.models import (
    Company,
    TechnicalSkill,
    SoftSkill,
    Technology,
    WorkExperience,
)
from work.serializers import (
    TechnicalSkillReadSerializer,
    SoftSkillReadSerializer,
)


@pytest.mark.django_db
class TestCompanyViews(AbstractModelViewsTest):
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
class TestTechnicalSkillViews(AbstractActiveModelViewsTest):
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
class TestSoftSkillViews(AbstractActiveModelViewsTest):
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


@pytest.mark.django_db
class TestTechnologyViews(AbstractActiveModelViewsTest):
    model = Technology
    list_url_name = "technology-list"
    retrieve_url_name = "technology-detail"
    payload = {
        "active": True,
        "name": "technology 1",
        "typology": "language",
        "level": 4,
    }
    update_key = "name"
    update_value = "technology 2"


@pytest.mark.django_db
class TestWorkExperienceViews(AbstractActiveModelViewsTest):
    model = WorkExperience
    list_url_name = "workexperience-list"
    retrieve_url_name = "workexperience-detail"
    update_key = "title"
    update_value = "title 2"

    def _get_company(self):
        if Company.objects.exists():
            return Company.objects.get()
        company = Company.objects.create(name="Company", website=None)
        return company

    def _get_technical_skills(self):
        if not TechnicalSkill.objects.exists():
            TechnicalSkill.objects.create(active=True, name="Tech Skill 1")
            TechnicalSkill.objects.create(active=True, name="Tech Skill 2")
            TechnicalSkill.objects.create(active=False, name="Tech Skill 3")
        return list(TechnicalSkill.objects.all())

    def _get_soft_skills(self):
        if not SoftSkill.objects.exists():
            SoftSkill.objects.create(active=True, name="Soft Skill 1")
            SoftSkill.objects.create(active=True, name="Soft Skill 2")
            SoftSkill.objects.create(active=False, name="Soft Skill 3")
        return list(SoftSkill.objects.all())

    def get_payload(self):
        company = self._get_company()
        tech_skills = self._get_technical_skills()
        soft_skills = self._get_soft_skills()
        payload = {
            "active": True,
            "title": "title 1",
            "description": "description",
            "company": str(company.uuid),
            "start_date": "01/01/2024",
            "end_date": None,
            "technical_skills": [
                str(tech_skill.uuid) for tech_skill in tech_skills
            ],
            "soft_skills": [str(soft_skill.uuid) for soft_skill in soft_skills],
        }
        return payload

    def create_object(self, **overrides):
        values = copy.deepcopy(self.get_payload())
        values.update(overrides)
        company_uuid = values.pop("company")
        company = Company.objects.get(uuid=company_uuid)
        values["company"] = company
        technical_skills_uuid = values.pop("technical_skills")
        technical_skills = TechnicalSkill.objects.filter(
            uuid__in=technical_skills_uuid
        )
        soft_skills_uuid = values.pop("soft_skills")
        soft_skills = SoftSkill.objects.filter(uuid__in=soft_skills_uuid)
        work_experiece = WorkExperience.objects.create(**values)
        work_experiece.technical_skills.add(*technical_skills)
        work_experiece.soft_skills.add(*soft_skills)
        return work_experiece

    def test_retrieve(self, staff_client):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = staff_client.get(url)
        assert r.json()[self.pk_key] == str(obj.uuid)
        obj_tech_skills = [
            TechnicalSkillReadSerializer(tech_skill).data
            for tech_skill in obj.technical_skills.all()
        ]
        assert r.json()["technical_skills"] == obj_tech_skills
        obj_soft_skills = [
            SoftSkillReadSerializer(soft_skill).data
            for soft_skill in obj.soft_skills.all()
        ]
        assert r.json()["soft_skills"] == obj_soft_skills

    def test_retrieve_no_staff(self):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = APIClient().get(url)
        assert r.json()[self.pk_key] == str(obj.uuid)
        obj_tech_skills = [
            TechnicalSkillReadSerializer(tech_skill).data
            for tech_skill in obj.technical_skills.filter(active=True)
        ]
        assert r.json()["technical_skills"] == obj_tech_skills
        obj_soft_skills = [
            SoftSkillReadSerializer(soft_skill).data
            for soft_skill in obj.soft_skills.filter(active=True)
        ]
        assert r.json()["soft_skills"] == obj_soft_skills

    def test_update_m2m(self, staff_client):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        payload = {}
        tech_skill_4 = TechnicalSkill.objects.create(
            active=True, name="Tech Skill 4"
        )
        tech_skill_5 = TechnicalSkill.objects.create(
            active=True, name="Tech Skill 5"
        )
        tech_skills_uuid = [str(tech_skill_4.uuid), str(tech_skill_5.uuid)]
        soft_skill_4 = SoftSkill.objects.create(
            active=True, name="Tech Skill 4"
        )
        soft_skill_5 = SoftSkill.objects.create(
            active=True, name="Tech Skill 5"
        )
        soft_skills_uuid = [str(soft_skill_4.uuid), str(soft_skill_5.uuid)]
        payload = self.get_payload()
        payload["technical_skills"] = tech_skills_uuid
        payload["soft_skills"] = soft_skills_uuid
        r = staff_client.put(
            url,
            payload,
            format="json",
        )
        assert r.status_code == 200
        updated_obj = WorkExperience.objects.get()
        updated_obj_tech_skills = updated_obj.technical_skills.all()
        updated_obj_soft_skills = updated_obj.soft_skills.all()
        assert [
            str(tech_skill.uuid) for tech_skill in updated_obj_tech_skills
        ] == tech_skills_uuid
        assert [
            str(soft_skill.uuid) for soft_skill in updated_obj_soft_skills
        ] == soft_skills_uuid
