from django.contrib import admin
from django.urls import path, include

from .views import health

from persona.urls import router as persona_router
from work.urls import router as work_router

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "health/",
        health,
        name="api-health",
    ),
    path("persona/", include(persona_router.urls)),
    path("work/", include(work_router.urls)),
]
