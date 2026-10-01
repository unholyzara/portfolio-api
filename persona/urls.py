from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

views.personal_info_views.register(router=router, prefix="personal-info")
views.overview_views.register(router=router, prefix="overviews")
views.spoken_language_views.register(router=router, prefix="spoken-language")
