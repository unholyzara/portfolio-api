from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

views.company_views.register(router=router, prefix="company")
views.skill_views.register(router=router, prefix="skills")
views.technology_views.register(router=router, prefix="technology")
views.work_experience_views.register(router=router, prefix="work-experiece")
views.project_views.register(router=router, prefix="project")
