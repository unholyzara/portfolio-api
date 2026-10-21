from rest_framework import generics, mixins, permissions
from django.shortcuts import get_object_or_404

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


class PersonalInfoView(
    mixins.CreateModelMixin,
    generics.RetrieveUpdateDestroyAPIView,
):
    queryset = PersonalInfo.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PersonalInfoReadSerializer
        return PersonalInfoWriteSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_object(self):
        obj = get_object_or_404(self.get_queryset())
        self.check_object_permissions(self.request, obj)
        return obj

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


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
