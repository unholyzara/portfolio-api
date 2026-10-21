from api.utils.views.models import ModelViews, Actions

from .models import (
    Company,
    TechnicalSkill,
    SoftSkill,
    Technology,
    WorkExperience,
)
from .serializers import (
    CompanyReadSerializer,
    CompanyWriteSerializer,
    TechnicalSkillReadSerializer,
    TechnicalSkillStaffReadSerializer,
    TechnicalWriteSkillSerializer,
    SoftSkillReadSerializer,
    SoftSkillStaffReadSerializer,
    SoftSkillWriteSerializer,
    TechnologyReadSerializer,
    TechnologyStaffReadSerializer,
    TechnologyWriteSerializer,
    WorkExperienceReadSerializer,
    WorkExperienceStaffReadSerializer,
    WorkExperienceWriteSerializer,
)

company_views = ModelViews(
    model=Company,
    read_serializer=CompanyReadSerializer,
    write_serializer=CompanyWriteSerializer,
    actions=(
        Actions.LIST,
        Actions.RETRIEVE,
        Actions.CREATE,
        Actions.UPDATE,
        Actions.DESTROY,
    ),
)

technical_skill_views = ModelViews(
    model=TechnicalSkill,
    read_serializer=TechnicalSkillReadSerializer,
    read_staff_serializer=TechnicalSkillStaffReadSerializer,
    write_serializer=TechnicalWriteSkillSerializer,
    actions=(
        Actions.LIST,
        Actions.RETRIEVE,
        Actions.CREATE,
        Actions.UPDATE,
        Actions.DESTROY,
    ),
)

soft_skill_views = ModelViews(
    model=SoftSkill,
    read_serializer=SoftSkillReadSerializer,
    read_staff_serializer=SoftSkillStaffReadSerializer,
    write_serializer=SoftSkillWriteSerializer,
    actions=(
        Actions.LIST,
        Actions.RETRIEVE,
        Actions.CREATE,
        Actions.UPDATE,
        Actions.DESTROY,
    ),
)

technology_views = ModelViews(
    model=Technology,
    read_serializer=TechnologyReadSerializer,
    read_staff_serializer=TechnologyStaffReadSerializer,
    write_serializer=TechnologyWriteSerializer,
    actions=(
        Actions.LIST,
        Actions.RETRIEVE,
        Actions.CREATE,
        Actions.UPDATE,
        Actions.DESTROY,
    ),
)

work_experience_views = ModelViews(
    model=WorkExperience,
    read_serializer=WorkExperienceReadSerializer,
    read_staff_serializer=WorkExperienceStaffReadSerializer,
    write_serializer=WorkExperienceWriteSerializer,
    actions=(
        Actions.LIST,
        Actions.RETRIEVE,
        Actions.CREATE,
        Actions.UPDATE,
        Actions.DESTROY,
    ),
    select_related=("company",),
    prefetch_related=("technical_skills", "soft_skills", "technologies"),
)
