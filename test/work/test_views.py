import copy

from datetime import date

import pytest

from rest_framework.test import APIClient

from test.utils.abstract import (
    AbstractModelViewsTest,
    AbstractStaffModelViewsTest,
    AbstractActiveModelViewsTest,
)

from work.models import (
    Company,
    SkillType,
    Skill,
    TechnologyType,
    Technology,
    WorkExperience,
    WorkResponsibility,
    Project,
    ProjectRepository,
)
from work.serializers import (
    SkillReadSerializer,
    SkillStaffReadSerializer,
    TechnologyReadSerializer,
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
class TestCompanyStaffViews(AbstractStaffModelViewsTest):
    model = Company
    list_url_name = "company-staff-list"
    retrieve_url_name = "company-staff-detail"
    payload = {
        "name": "company 1",
        "website": None,
    }
    update_key = "name"
    update_value = "company 2"


@pytest.mark.django_db
class TestSkillViews(AbstractActiveModelViewsTest):
    model = Skill
    list_url_name = "skill-list"
    retrieve_url_name = "skill-detail"
    payload = {
        "active": True,
        "name": "technicalskill 1",
        "description": "description",
        "typology": SkillType.TECHNICAL,
    }
    update_key = "name"
    update_value = "technicalskill 2"


@pytest.mark.django_db
class TestSkillStaffViews(AbstractStaffModelViewsTest):
    model = Skill
    list_url_name = "skill-staff-list"
    retrieve_url_name = "skill-staff-detail"
    payload = {
        "active": True,
        "name_it": "technicalskill 1",
        "description_it": "description",
        "typology": SkillType.TECHNICAL,
    }
    update_key = "name_it"
    update_value = "technicalskill 2"


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
class TestStaffTechnologyViews(AbstractStaffModelViewsTest):
    model = Technology
    list_url_name = "technology-staff-list"
    retrieve_url_name = "technology-staff-detail"
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
    list_url_name = "work-experience-list"
    retrieve_url_name = "work-experience-detail"
    update_key = "title"
    update_value = "title 2"

    def _get_company(self):
        if Company.objects.exists():
            return Company.objects.get()
        company = Company.objects.create(name="Company", website=None)
        return company

    def _get_technical_skills(self):
        if not Skill.objects.exists():
            Skill.objects.create(
                active=True, name="Tech Skill 1", typology=SkillType.TECHNICAL
            )
            Skill.objects.create(
                active=True, name="Tech Skill 2", typology=SkillType.TECHNICAL
            )
            Skill.objects.create(
                active=False, name="Tech Skill 3", typology=SkillType.TECHNICAL
            )
        return list(Skill.objects.filter(typology=SkillType.TECHNICAL))

    def _get_soft_skills(self):
        if not Skill.objects.exists():
            Skill.objects.create(
                active=True, name="Soft Skill 1", typology=SkillType.SOFT
            )
            Skill.objects.create(
                active=True, name="Soft Skill 2", typology=SkillType.SOFT
            )
            Skill.objects.create(
                active=False, name="Soft Skill 3", typology=SkillType.SOFT
            )
        return list(Skill.objects.filter(typology=SkillType.SOFT))

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
        technical_skills = Skill.objects.filter(
            uuid__in=technical_skills_uuid, typology=SkillType.TECHNICAL
        )
        soft_skills_uuid = values.pop("soft_skills")
        soft_skills = Skill.objects.filter(
            uuid__in=soft_skills_uuid, typology=SkillType.SOFT
        )
        work_experiece = WorkExperience.objects.create(**values)
        work_experiece.technical_skills.add(*technical_skills)
        work_experiece.soft_skills.add(*soft_skills)
        return work_experiece

    def test_retrieve(self):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = APIClient().get(url)
        response_data = r.json()
        assert response_data[self.pk_key] == str(obj.uuid)
        obj_tech_skills = [
            SkillReadSerializer(tech_skill).data
            for tech_skill in obj.technical_skills.filter(active=True)
        ]
        assert response_data["technical_skills"] == obj_tech_skills
        obj_soft_skills = [
            SkillReadSerializer(soft_skill).data
            for soft_skill in obj.soft_skills.filter(active=True)
        ]
        assert response_data["soft_skills"] == obj_soft_skills


@pytest.mark.django_db
class TestWorkExperienceStaffViews(AbstractStaffModelViewsTest):
    model = WorkExperience
    list_url_name = "work-experience-staff-list"
    retrieve_url_name = "work-experience-staff-detail"
    update_key = "title_it"
    update_value = "title 2"

    def _get_company(self):
        if Company.objects.exists():
            return Company.objects.get()
        company = Company.objects.create(name="Company", website=None)
        return company

    def _get_technical_skills(self):
        if not Skill.objects.exists():
            Skill.objects.create(
                active=True, name="Tech Skill 1", typology=SkillType.TECHNICAL
            )
            Skill.objects.create(
                active=True, name="Tech Skill 2", typology=SkillType.TECHNICAL
            )
            Skill.objects.create(
                active=False, name="Tech Skill 3", typology=SkillType.TECHNICAL
            )
        return list(Skill.objects.filter(typology=SkillType.TECHNICAL))

    def _get_soft_skills(self):
        if not Skill.objects.exists():
            Skill.objects.create(
                active=True, name="Soft Skill 1", typology=SkillType.SOFT
            )
            Skill.objects.create(
                active=True, name="Soft Skill 2", typology=SkillType.SOFT
            )
            Skill.objects.create(
                active=False, name="Soft Skill 3", typology=SkillType.SOFT
            )
        return list(Skill.objects.filter(typology=SkillType.SOFT))

    def get_payload(self):
        company = self._get_company()
        tech_skills = self._get_technical_skills()
        soft_skills = self._get_soft_skills()
        payload = {
            "active": True,
            "title_it": "title 1",
            "description_it": "description",
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
        technical_skills = Skill.objects.filter(
            uuid__in=technical_skills_uuid, typology=SkillType.TECHNICAL
        )
        soft_skills_uuid = values.pop("soft_skills")
        soft_skills = Skill.objects.filter(
            uuid__in=soft_skills_uuid, typology=SkillType.SOFT
        )
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
            SkillStaffReadSerializer(tech_skill).data
            for tech_skill in obj.technical_skills.all()
        ]
        assert r.json()["technical_skills"] == obj_tech_skills
        obj_soft_skills = [
            SkillStaffReadSerializer(soft_skill).data
            for soft_skill in obj.soft_skills.all()
        ]
        assert r.json()["soft_skills"] == obj_soft_skills

    def test_update_m2m(self, staff_client):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        payload = {}
        tech_skill_4 = Skill.objects.create(
            active=True, name="Tech Skill 4", typology=SkillType.TECHNICAL
        )
        tech_skill_5 = Skill.objects.create(
            active=True, name="Tech Skill 5", typology=SkillType.TECHNICAL
        )
        tech_skills_uuid = [str(tech_skill_4.uuid), str(tech_skill_5.uuid)]
        soft_skill_4 = Skill.objects.create(
            active=True, name="Soft Skill 4", typology=SkillType.SOFT
        )
        soft_skill_5 = Skill.objects.create(
            active=True, name="Soft Skill 5", typology=SkillType.SOFT
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


@pytest.mark.django_db
class TestWorkResponsibilityViews(AbstractActiveModelViewsTest):
    model = WorkResponsibility
    list_url_name = "work-responsibility-list"
    retrieve_url_name = "work-responsibility-detail"
    update_key = "description_it"
    update_value = "descritpion IT 2"

    def _get_company(self):
        if Company.objects.exists():
            return Company.objects.get()
        company = Company.objects.create(name="Company", website=None)
        return company

    def _get_work_experience(self):
        if WorkExperience.objects.exists():
            return WorkExperience.objects.get()
        company = self._get_company()
        work_experience = WorkExperience.objects.create(
            active=True,
            title="work experience",
            company=company,
            start_date=date(day=1, month=1, year=2024),
        )
        return work_experience

    def get_payload(self):
        work_experience = self._get_work_experience()
        payload = {
            "active": True,
            "description_it": "description",
            "work_experience": str(work_experience.uuid),
            "order": WorkResponsibility.objects.count() + 1,
        }
        return payload

    def create_object(self, **overrides):
        values = copy.deepcopy(self.get_payload())
        values.update(overrides)
        work_experience_uuid = values.pop("work_experience")
        work_experience = WorkExperience.objects.get(uuid=work_experience_uuid)
        values["work_experience"] = work_experience
        work_responsibility = WorkResponsibility.objects.create(**values)
        return work_responsibility


@pytest.mark.django_db
class TestWorkResponsibilityStaffViews(AbstractStaffModelViewsTest):
    model = WorkResponsibility
    list_url_name = "work-responsibility-staff-list"
    retrieve_url_name = "work-responsibility-staff-detail"
    update_key = "description_it"
    update_value = "descritpion IT 2"

    def _get_company(self):
        if Company.objects.exists():
            return Company.objects.get()
        company = Company.objects.create(name="Company", website=None)
        return company

    def _get_work_experience(self):
        if WorkExperience.objects.exists():
            return WorkExperience.objects.get()
        company = self._get_company()
        work_experience = WorkExperience.objects.create(
            title="work experience",
            company=company,
            start_date=date(day=1, month=1, year=2024),
        )
        return work_experience

    def get_payload(self):
        work_experience = self._get_work_experience()
        payload = {
            "active": True,
            "description_it": "description",
            "work_experience": str(work_experience.uuid),
            "order": WorkResponsibility.objects.count() + 1,
        }
        return payload

    def create_object(self, **overrides):
        values = copy.deepcopy(self.get_payload())
        values.update(overrides)
        work_experience_uuid = values.pop("work_experience")
        work_experience = WorkExperience.objects.get(uuid=work_experience_uuid)
        values["work_experience"] = work_experience
        work_responsibility = WorkResponsibility.objects.create(**values)
        return work_responsibility


@pytest.mark.django_db
class TestProjectViews(AbstractActiveModelViewsTest):
    model = Project
    list_url_name = "project-list"
    retrieve_url_name = "project-detail"
    update_key = "title"
    update_value = "title 2"

    def _get_company(self):
        if Company.objects.exists():
            return Company.objects.get()
        company = Company.objects.create(name="Company", website=None)
        return company

    def _get_work_experience(self):
        if WorkExperience.objects.exists():
            return WorkExperience.objects.get()
        company = self._get_company()
        work_experience = WorkExperience.objects.create(
            title="work experience",
            company=company,
            start_date=date(day=1, month=1, year=2024),
        )
        return work_experience

    def _get_technologies(self):
        if not Technology.objects.exists():
            Technology.objects.create(
                name="Technology 1",
                typology=TechnologyType.LANGUAGE,
                level=4,
                active=True,
            )
            Technology.objects.create(
                name="Technology 2",
                typology=TechnologyType.LANGUAGE,
                level=4,
                active=True,
            )
        return list(Technology.objects.all())

    def get_payload(self):
        work_experience = self._get_work_experience()
        technologies = self._get_technologies()
        payload = {
            "active": True,
            "title": "title 1",
            "description": "description",
            "technologies": [str(tech.uuid) for tech in technologies],
            "work_experience": str(work_experience.uuid),
        }
        return payload

    def create_object(self, **overrides):
        values = copy.deepcopy(self.get_payload())
        values.update(overrides)
        work_experience_uuid = values.pop("work_experience")
        work_experience = WorkExperience.objects.get(uuid=work_experience_uuid)
        values["work_experience"] = work_experience
        technologies_uuid = values.pop("technologies")
        technologies = Technology.objects.filter(uuid__in=technologies_uuid)
        project = Project.objects.create(**values)
        project.technologies.add(*technologies)
        return project

    def test_retrieve(self):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = APIClient().get(url)
        assert r.json()[self.pk_key] == str(obj.uuid)
        obj_technologies = [
            TechnologyReadSerializer(tech).data
            for tech in obj.technologies.filter(active=True)
        ]
        assert r.json()["technologies"] == obj_technologies


@pytest.mark.django_db
class TestProjectStaffViews(AbstractStaffModelViewsTest):
    model = Project
    list_url_name = "project-staff-list"
    retrieve_url_name = "project-staff-detail"
    update_key = "title_it"
    update_value = "title 2"

    def _get_company(self):
        if Company.objects.exists():
            return Company.objects.get()
        company = Company.objects.create(name="Company", website=None)
        return company

    def _get_work_experience(self):
        if WorkExperience.objects.exists():
            return WorkExperience.objects.get()
        company = self._get_company()
        work_experience = WorkExperience.objects.create(
            title="work experience",
            company=company,
            start_date=date(day=1, month=1, year=2024),
        )
        return work_experience

    def _get_technologies(self):
        if not Technology.objects.exists():
            Technology.objects.create(
                name="Technology 1", typology=TechnologyType.LANGUAGE, level=4
            )
            Technology.objects.create(
                name="Technology 2", typology=TechnologyType.LANGUAGE, level=4
            )
        return list(Technology.objects.all())

    def get_payload(self):
        work_experience = self._get_work_experience()
        technologies = self._get_technologies()
        payload = {
            "active": True,
            "title_it": "title 1",
            "description_it": "description",
            "technologies": [str(tech.uuid) for tech in technologies],
            "work_experience": str(work_experience.uuid),
        }
        return payload

    def create_object(self, **overrides):
        values = copy.deepcopy(self.get_payload())
        values.update(overrides)
        work_experience_uuid = values.pop("work_experience")
        work_experience = WorkExperience.objects.get(uuid=work_experience_uuid)
        values["work_experience"] = work_experience
        technologies_uuid = values.pop("technologies")
        technologies = Technology.objects.filter(uuid__in=technologies_uuid)
        project = Project.objects.create(**values)
        project.technologies.add(*technologies)
        return project

    def test_retrieve(self, staff_client):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        r = staff_client.get(url)
        assert r.json()[self.pk_key] == str(obj.uuid)
        obj_technologies = [
            TechnologyReadSerializer(tech).data
            for tech in obj.technologies.all()
        ]
        assert r.json()["technologies"] == obj_technologies

    def test_update_m2m(self, staff_client):
        obj = self.create_object()
        url = self._get_detail_url(pk_value=obj.uuid)
        payload = {}
        tech_4 = Technology.objects.create(
            name="Technology 4", typology=TechnologyType.LANGUAGE, level=4
        )
        tech_5 = Technology.objects.create(
            name="Technology 5", typology=TechnologyType.LANGUAGE, level=4
        )
        technologies_uuid = [str(tech_4.uuid), str(tech_5.uuid)]
        payload = self.get_payload()
        payload["technologies"] = technologies_uuid
        r = staff_client.put(
            url,
            payload,
            format="json",
        )
        assert r.status_code == 200
        updated_obj = Project.objects.get()
        updated_obj_technologies = updated_obj.technologies.all()
        assert [
            str(tech.uuid) for tech in updated_obj_technologies
        ] == technologies_uuid


@pytest.mark.django_db
class TestProjectRepositoryViews(AbstractModelViewsTest):
    model = ProjectRepository
    list_url_name = "project-repository-list"
    retrieve_url_name = "project-repository-detail"
    update_key = "label"
    update_value = "label 2"

    def _get_project(self, active: bool = True):
        if Project.objects.filter(active=active).exists():
            return Project.objects.filter(active=active).get()
        title_n = Project.objects.all().count()
        project = Project.objects.create(
            title=f"Project {title_n +1}", active=active
        )
        return project

    def get_payload(self):
        project = self._get_project()
        payload = {
            "project": str(project.uuid),
            "url": "https://github.com/unholyzara/portfolio-api",
            "label": "label",
        }
        return payload

    def create_object(self, **overrides):
        values = copy.deepcopy(self.get_payload())
        values.update(overrides)
        project_uuid = values.pop("project")
        project = Project.objects.get(uuid=project_uuid)
        values["project"] = project  # type: ignore
        project_repository = ProjectRepository.objects.create(**values)
        return project_repository

    def test_list_project_not_active(self):
        first_obj = self.create_object()
        project_not_active = self._get_project(active=False)
        self.create_object(
            **{
                self.update_key: self.update_value,
                "project": str(project_not_active.uuid),
            }
        )
        r = APIClient().get(self.list_url)
        assert r.status_code == 200
        assert [obj[self.pk_key] for obj in r.json()] == [
            str(first_obj.uuid),
        ]


@pytest.mark.django_db
class TestProjectRepositoryStaffViews(AbstractStaffModelViewsTest):
    model = ProjectRepository
    list_url_name = "project-repository-staff-list"
    retrieve_url_name = "project-repository-staff-detail"
    update_key = "label"
    update_value = "label 2"

    def _get_project(self):
        if Project.objects.exists():
            return Project.objects.get()
        project = Project.objects.create(title="Project")
        return project

    def get_payload(self):
        project = self._get_project()
        payload = {
            "project": str(project.uuid),
            "url": "https://github.com/unholyzara/portfolio-api",
            "label": "label",
        }
        return payload

    def create_object(self, **overrides):
        values = copy.deepcopy(self.get_payload())
        values.update(overrides)
        project_uuid = values.pop("project")
        project = Project.objects.get(uuid=project_uuid)
        values["project"] = project  # type: ignore
        project_repository = ProjectRepository.objects.create(**values)
        return project_repository
