from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Overview, PersonalInfo, SpokenLanguage
from .serializers import (
    OverviewSerializer,
    PersonalInfoSerializer,
    SpokenLanguageSerializer,
)
from api.utils.views.models import ActiveModelViews


@api_view(["GET"])
def health(request: Request) -> Response:
    return Response({"status": "ok"})


@api_view(["GET"])
def get_personal_info(request: Request) -> Response:
    obj = get_object_or_404(PersonalInfo)
    serialized = PersonalInfoSerializer(obj)
    return Response(serialized.data)


overview_views = ActiveModelViews(
    model=Overview,
    serializer=OverviewSerializer,
)

spoken_language_views = ActiveModelViews(
    model=SpokenLanguage,
    serializer=SpokenLanguageSerializer,
)
