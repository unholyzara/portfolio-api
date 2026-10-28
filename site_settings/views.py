from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from api.utils.views.models import StaffModelViews, Actions

from .models import SiteSettings
from .serializers import (
    SiteSettingsStaffReadSerializer,
    SiteSettingsStaffWriteSerializer,
)


@api_view(["GET"])
@permission_classes([AllowAny])
def site_status(request: Request):
    maintenance = SiteSettings.is_maintenance()
    data = {"maintenance": maintenance, "bypass": request.user.is_staff}
    if maintenance:
        current = SiteSettings.objects.get()
        data["message"] = current.maintenance_message
    return Response(data)


site_settings_staff_views = StaffModelViews(
    model=SiteSettings,
    read_serializer=SiteSettingsStaffReadSerializer,
    write_serializer=SiteSettingsStaffWriteSerializer,
    actions=(Actions.LIST, Actions.RETRIEVE, Actions.UPDATE),
)
