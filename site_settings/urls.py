from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

views.site_settings_staff_views.register(
    router=router, prefix="site-settings-staff"
)

urlpatterns = [
    path("site-status/", views.site_status, name="site-status"),
    *router.urls,
]
