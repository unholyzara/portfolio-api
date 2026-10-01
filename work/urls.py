from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

views.company_skill_views.register(router=router, prefix="company")
views.technical_skill_views.register(router=router, prefix="technical-skills")
views.soft_skill_views.register(router=router, prefix="soft-skills")
views.work_experience_views.register(router=router, prefix="work-experiece")
