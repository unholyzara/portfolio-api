from .models import Overview, PersonalInfo, SpokenLanguage
from .serializers import (
    PersonalInfoReadSerializer,
    PersonalInfoWriteSerializer,
    OverviewReadSerializer,
    OverviewWriteSerializer,
    SpokenLanguageReadSerializer,
    SpokenLanguageWriteSerializer,
)
from api.utils.views.models import ModelViews, Actions

personal_info_views = ModelViews(
    model=PersonalInfo,
    read_serializer=PersonalInfoReadSerializer,
    write_serializer=PersonalInfoWriteSerializer,
    actions=(
        Actions.LIST,
        Actions.RETRIEVE,
        Actions.CREATE,
        Actions.UPDATE,
        Actions.DESTROY,
    ),
)

overview_views = ModelViews(
    model=Overview,
    read_serializer=OverviewReadSerializer,
    write_serializer=OverviewWriteSerializer,
    actions=(
        Actions.LIST,
        Actions.RETRIEVE,
        Actions.CREATE,
        Actions.UPDATE,
        Actions.DESTROY,
    ),
)

spoken_language_views = ModelViews(
    model=SpokenLanguage,
    read_serializer=SpokenLanguageReadSerializer,
    write_serializer=SpokenLanguageWriteSerializer,
    actions=(
        Actions.LIST,
        Actions.RETRIEVE,
        Actions.CREATE,
        Actions.UPDATE,
        Actions.DESTROY,
    ),
)
