from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

views.overview_views.register(router=router, prefix="overviews")
views.spoken_language_views.register(router=router, prefix="spoken-language")

urlpatterns = [
    path(
        "personal-info/", views.PersonalInfoView.as_view(), name="personalinfo"
    ),
    *router.urls,
]
