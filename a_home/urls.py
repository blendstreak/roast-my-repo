from django.urls import path

from .views import home_view, roast_repo_view, generate_readme_view

urlpatterns = [
        path('', home_view, name='home'),
        path('roast_repo/', roast_repo_view, name="roast_repo"),
        path('rescue/', generate_readme_view, name="generate_readme"),
]
