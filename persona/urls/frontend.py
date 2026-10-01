from django.urls import path
from persona import views

urlpatterns = [
    path(
        "personal-info/",
        views.get_personal_info,
        name="personal-info-info-fe",
    ),
    path(
        "overviews/",
        views.overview_views.list_endpoint(fe_flag=True),
        name="overview-list-fe",
    ),
    path(
        "overviews/detail/",
        views.overview_views.detail_endpoint(fe_flag=True),
        name="overview-detail-fe",
    ),
    path(
        "spoken-languages/",
        views.spoken_language_views.list_endpoint(fe_flag=True),
        name="spoken-language-list-fe",
    ),
    path(
        "spoken-languages/detail/",
        views.spoken_language_views.detail_endpoint(fe_flag=True),
        name="spoken-language-detail-fe",
    ),
]
