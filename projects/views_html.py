from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Project

@login_required
def project_list(request):
    proyectos = Project.objects.all()
    return render(request, "projects/list.html", {"proyectos": proyectos})
