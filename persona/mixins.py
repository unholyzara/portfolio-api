from rest_framework import generics
from django.shortcuts import get_object_or_404

from .models import PersonalInfo


class PersonalInfoMixin(generics.GenericAPIView):
    queryset = PersonalInfo.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset())
        self.check_object_permissions(self.request, obj)
        return obj
