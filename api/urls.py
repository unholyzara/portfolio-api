from django.contrib import admin
from django.urls import path, include

from .views import health

from work.urls import router as work_router

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "health/",
        health,
        name="api-health",
    ),
    path("persona/", include("persona.urls")),
    path("work/", include(work_router.urls)),
]
