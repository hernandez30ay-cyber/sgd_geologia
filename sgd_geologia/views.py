from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from projects.models import Project
from documents.models import Document

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )
        if user:
            login(request, user)
            return redirect("home")
    return render(request, "login.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def home(request):
    total_projects = Project.objects.count()
    total_documents = Document.objects.count()
    recent_projects = Project.objects.order_by("-id")[:5]
    recent_documents = Document.objects.order_by("-id")[:5]

    return render(request, "dashboard.html", {
        "total_projects": total_projects,
        "total_documents": total_documents,
        "recent_projects": recent_projects,
        "recent_documents": recent_documents,
    })

@login_required
def projects_view(request):
    proyectos = Project.objects.all()
    return render(request, "projects/list.html", {"projects": proyectos})

@login_required
def documents_view(request):
    documentos = Document.objects.filter(eliminado=False)
    return render(request, "documents/list.html", {"documents": documentos})

@login_required
def chatbot_ui(request):
    from documents.models import Document
    docs = Document.objects.filter(eliminado=False)
    return render(request, "chatbot/ui.html", {"documents": docs})
