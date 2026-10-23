from api.utils.views.models import ModelViews, StaffModelViews

from .models import (
    Company,
    Skill,
    Technology,
    WorkExperience,
    Project,
)
from .serializers import (
    CompanyReadSerializer,
    CompanyWriteSerializer,
    SkillReadSerializer,
    SkillStaffReadSerializer,
    SkillWriteSerializer,
    TechnologyReadSerializer,
    TechnologyStaffReadSerializer,
    TechnologyWriteSerializer,
    WorkExperienceReadSerializer,
    WorkExperienceStaffReadSerializer,
    WorkExperienceWriteSerializer,
    ProjectReadSerializer,
    ProjectStaffReadSerializer,
    ProjectWriteSerializer,
)

company_views = ModelViews(
    model=Company,
    read_serializer=CompanyReadSerializer,
)
company_staff_views = StaffModelViews(
    model=Company,
    read_serializer=CompanyReadSerializer,
    write_serializer=CompanyWriteSerializer,
)

skill_views = ModelViews(
    model=Skill,
    read_serializer=SkillReadSerializer,
)
skill_staff_views = StaffModelViews(
    model=Skill,
    read_serializer=SkillStaffReadSerializer,
    write_serializer=SkillWriteSerializer,
)

technology_views = ModelViews(
    model=Technology,
    read_serializer=TechnologyReadSerializer,
)
technology_staff_views = StaffModelViews(
    model=Technology,
    read_serializer=TechnologyStaffReadSerializer,
    write_serializer=TechnologyWriteSerializer,
)

work_experience_views = ModelViews(
    model=WorkExperience,
    read_serializer=WorkExperienceReadSerializer,
    select_related=("company",),
    prefetch_related=("technical_skills", "soft_skills", "technologies"),
)
work_experience_staff_views = StaffModelViews(
    model=WorkExperience,
    read_serializer=WorkExperienceStaffReadSerializer,
    write_serializer=WorkExperienceWriteSerializer,
    select_related=("company",),
    prefetch_related=("technical_skills", "soft_skills", "technologies"),
)

project_views = ModelViews(
    model=Project,
    read_serializer=ProjectReadSerializer,
    select_related=("work_experience",),
    prefetch_related=("technologies",),
)
project_staff_views = StaffModelViews(
    model=Project,
    read_serializer=ProjectStaffReadSerializer,
    write_serializer=ProjectWriteSerializer,
    select_related=("work_experience",),
    prefetch_related=("technologies",),
)
