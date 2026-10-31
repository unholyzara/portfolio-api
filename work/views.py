from api.utils.views.models import ModelViews, StaffModelViews

from .models import (
    Company,
    Skill,
    Technology,
    WorkExperience,
    Project,
    WorkResponsibility,
    ProjectRepository,
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
    WorkResponsibilityReadSerializer,
    WorkResponsibilityStaffReadSerializer,
    WorkResponsibilityWriteSerializer,
    ProjectReadSerializer,
    ProjectStaffReadSerializer,
    ProjectWriteSerializer,
    ProjectRepositoryReadSerializer,
    ProjectRepositoryWriteSerializer,
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

work_responsibility_views = ModelViews(
    model=WorkResponsibility,
    read_serializer=WorkResponsibilityReadSerializer,
    select_related=("work_experience",),
)
work_responsibility_staff_views = StaffModelViews(
    model=WorkResponsibility,
    read_serializer=WorkResponsibilityStaffReadSerializer,
    write_serializer=WorkResponsibilityWriteSerializer,
    select_related=("work_experience",),
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

project_repository_views = ModelViews(
    model=ProjectRepository,
    read_serializer=ProjectRepositoryReadSerializer,
    select_related=("project",),
    queryset=ProjectRepository.objects.filter(project__active=True).distinct(),
)
project_repository_staff_views = StaffModelViews(
    model=ProjectRepository,
    read_serializer=ProjectRepositoryReadSerializer,
    write_serializer=ProjectRepositoryWriteSerializer,
    select_related=("project",),
)
