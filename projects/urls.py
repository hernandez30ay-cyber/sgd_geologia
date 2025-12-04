from django.urls import path
from .views_html import project_list

urlpatterns = [
    path("", project_list, name="project_list"),
]
