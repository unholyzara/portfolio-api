from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

views.company_views.register(router=router, prefix="company")
views.company_staff_views.register(router=router, prefix="company-staff")

views.skill_views.register(router=router, prefix="skill")
views.skill_staff_views.register(router=router, prefix="skill-staff")

views.technology_views.register(router=router, prefix="technology")
views.technology_staff_views.register(router=router, prefix="technology-staff")

views.work_experience_views.register(router=router, prefix="work-experiece")
views.work_experience_staff_views.register(
    router=router, prefix="work-experiece-staff"
)

views.project_views.register(router=router, prefix="project")
views.project_staff_views.register(router=router, prefix="project-staff")

views.project_repository_views.register(
    router=router, prefix="project-repository"
)
views.project_repository_staff_views.register(
    router=router, prefix="project-repository-staff"
)
