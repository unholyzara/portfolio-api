from api.utils.views.models import ModelViews, Actions

from .models import Company, TechnicalSkill, SoftSkill, WorkExperience
from .serializers import (
    CompanyReadSerializer,
    CompanyWriteSerializer,
    TechnicalReadSkillSerializer,
    TechnicalWriteSkillSerializer,
    SoftSkillReadSerializer,
    SoftSkillWriteSerializer,
    WorkExperienceReadSerializer,
    WorkExperienceWriteSerializer,
)

company_skill_views = ModelViews(
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
    read_serializer=TechnicalReadSkillSerializer,
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
    write_serializer=SoftSkillWriteSerializer,
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
    write_serializer=WorkExperienceWriteSerializer,
    actions=(
        Actions.LIST,
        Actions.RETRIEVE,
        Actions.CREATE,
        Actions.UPDATE,
        Actions.DESTROY,
    ),
    select_related=("company",),
    prefetch_related=("technical_skills", "soft_skills"),
)
