from rest_framework import generics, mixins, permissions

from .models import Overview, SpokenLanguage, Education
from .serializers import (
    PersonalInfoReadSerializer,
    PersonalInfoWriteSerializer,
    OverviewReadSerializer,
    OverviewStaffReadSerializer,
    OverviewWriteSerializer,
    SpokenLanguageReadSerializer,
    SpokenLanguageStaffReadSerializer,
    SpokenLanguageWriteSerializer,
    EducationReadSerializer,
    EducationStaffReadSerializer,
    EducationWriteSerializer,
)
from api.utils.views.models import ModelViews, StaffModelViews

from .mixins import PersonalInfoMixin
from .exceptions import PersonalInfoAlreadyExists


class PersonalInfoView(PersonalInfoMixin, generics.RetrieveAPIView):
    serializer_class = PersonalInfoReadSerializer
    permission_classes = [permissions.AllowAny]


class PersonalInfoStaffView(
    PersonalInfoMixin,
    mixins.CreateModelMixin,
    generics.RetrieveUpdateDestroyAPIView,
):
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PersonalInfoReadSerializer
        return PersonalInfoWriteSerializer

    def post(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            raise PersonalInfoAlreadyExists()
        return self.create(request, *args, **kwargs)


overview_views = ModelViews(
    model=Overview,
    read_serializer=OverviewReadSerializer,
)
overview_staff_views = StaffModelViews(
    model=Overview,
    read_serializer=OverviewStaffReadSerializer,
    write_serializer=OverviewWriteSerializer,
)

spoken_language_views = ModelViews(
    model=SpokenLanguage,
    read_serializer=SpokenLanguageReadSerializer,
)
spoken_language_staff_views = StaffModelViews(
    model=SpokenLanguage,
    read_serializer=SpokenLanguageStaffReadSerializer,
    write_serializer=SpokenLanguageWriteSerializer,
)

education_views = ModelViews(
    model=Education,
    read_serializer=EducationReadSerializer,
)
education_staff_views = StaffModelViews(
    model=Education,
    read_serializer=EducationStaffReadSerializer,
    write_serializer=EducationWriteSerializer,
)
