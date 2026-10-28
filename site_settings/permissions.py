from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission

from .models import SiteSettings


class MaintenanceException(APIException):
    status_code = 503
    default_detail = "maintenance"
    default_code = "maintenance"


class MaintenancePermission(BasePermission):
    def has_permission(self, request, view):
        if not SiteSettings.is_maintenance():
            return True
        if request.user and request.user.is_staff:
            return True
        raise MaintenanceException()
