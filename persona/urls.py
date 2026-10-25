from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

views.overview_views.register(router=router, prefix="overview")
views.overview_staff_views.register(router=router, prefix="overview-staff")
views.spoken_language_views.register(router=router, prefix="spoken-language")
views.spoken_language_staff_views.register(
    router=router, prefix="spoken-language-staff"
)
views.education_views.register(router=router, prefix="education")
views.education_staff_views.register(router=router, prefix="education-staff")

urlpatterns = [
    path(
        "personal-info/", views.PersonalInfoView.as_view(), name="personalinfo"
    ),
    path(
        "personal-info-staff/",
        views.PersonalInfoStaffView.as_view(),
        name="personalinfo-staff",
    ),
    *router.urls,
]
