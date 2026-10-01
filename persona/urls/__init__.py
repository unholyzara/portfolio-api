from django.urls import path, include

from persona import views

urlpatterns = [
    path(
        "health/",
        views.health,
        name="api-health",
    ),
    path(
        "back-office/",
        include(
            "persona.urls.backoffice",
        ),
    ),
    path(
        "fe/",
        include(
            "persona.urls.frontend",
        ),
    ),
]
