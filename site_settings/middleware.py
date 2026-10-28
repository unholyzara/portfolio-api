from django.http import JsonResponse

from .models import SiteSettings

ALLOWED_PREFIXES = ("/api/site-status/", "/api/auth/", "/admin/", "/static/")


class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(ALLOWED_PREFIXES):
            return self.get_response(request)
        if SiteSettings.is_maintenance() and not request.user.is_staff:
            return JsonResponse(
                {"detail": "maintenance"},
                status=503,
            )
        return self.get_response(request)
