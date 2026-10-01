from django.urls import path
from persona import views

urlpatterns = [
    path(
        "personal-info/",
        views.get_personal_info,
        name="personal-info-info-backoffice",
    ),
    path(
        "overviews/",
        views.overview_views.list_endpoint(),
        name="overview-list-backoffice",
    ),
    path(
        "overviews/detail/",
        views.overview_views.detail_endpoint(),
        name="overview-detail-backoffice",
    ),
    path(
        "spoken-languages/",
        views.spoken_language_views.list_endpoint(),
        name="spoken-language-list-backoffice",
    ),
    path(
        "spoken-languages/detail/",
        views.spoken_language_views.detail_endpoint(),
        name="spoken-language-detail-backoffice",
    ),
]
