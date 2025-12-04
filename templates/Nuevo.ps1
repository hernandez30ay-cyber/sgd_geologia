Write-Host "=== Configurando UI completa del SGD ==="

# 1. Rutas de archivos importantes
$projectFolder = ".\sgd_geologia"
$urlsPath      = "$projectFolder\urls.py"
$viewsPath     = "$projectFolder\views.py"
$settingsPath  = "$projectFolder\settings.py"

# 2. Crear carpetas de templates
New-Item -ItemType Directory -Force ".\templates"         | Out-Null
New-Item -ItemType Directory -Force ".\templates\auth"    | Out-Null
New-Item -ItemType Directory -Force ".\templates\projects"| Out-Null
New-Item -ItemType Directory -Force ".\templates\documents" | Out-Null
New-Item -ItemType Directory -Force ".\templates\chatbot" | Out-Null

# 3. base.html con menu
@'
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>SGD Marvin Valle</title>
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
        <a class="navbar-brand" href="/">SGD Marvin Valle</a>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                data-bs-target="#navbarNav" aria-controls="navbarNav"
                aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav me-auto">

                <li class="nav-item">
                    <a class="nav-link" href="/">Inicio</a>
                </li>

                <li class="nav-item">
                    <a class="nav-link" href="/projects/">Proyectos</a>
                </li>

                <li class="nav-item">
                    <a class="nav-link" href="/documents/">Documentos</a>
                </li>

                <li class="nav-item">
                    <a class="nav-link" href="/chatbot_ui/">Chatbot</a>
                </li>

            </ul>

            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link text-danger" href="/logout/">Cerrar sesion</a>
                </li>
            </ul>
        </div>

    </div>
</nav>

<div class="container mt-4">
    {% block content %}{% endblock %}
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'@ | Set-Content -Encoding UTF8 ".\templates\base.html"

Write-Host "✔ base.html creado"

# 4. dashboard.html (home)
@'
{% extends "base.html" %}
{% block content %}
<h1>Panel de Gestion Documental</h1>
<p>Bienvenido al Sistema de Gestion Documental de la Consultoria Geologica Marvin Valle.</p>
{% endblock %}
'@ | Set-Content -Encoding UTF8 ".\templates\dashboard.html"

Write-Host "✔ dashboard.html creado"

# 5. login.html
@'
{% extends "base.html" %}
{% block content %}
<div class="row justify-content-center mt-5">
  <div class="col-md-4">
    <h3 class="text-center mb-3">Iniciar Sesion</h3>

    {% if messages %}
    <div class="alert alert-danger">
      {% for msg in messages %}{{ msg }}{% endfor %}
    </div>
    {% endif %}

    <form method="POST">
      {% csrf_token %}

      <div class="mb-3">
        <label>Usuario</label>
        <input class="form-control" type="text" name="username" required>
      </div>

      <div class="mb-3">
        <label>Contrasena</label>
        <input class="form-control" type="password" name="password" required>
      </div>

      <button class="btn btn-primary w-100" type="submit">Entrar</button>
    </form>
  </div>
</div>
{% endblock %}
'@ | Set-Content -Encoding UTF8 ".\templates\auth\login.html"

Write-Host "✔ login.html creado"

# 6. projects/list.html
@'
{% extends "base.html" %}
{% block content %}

<h2>Proyectos</h2>

<table class="table table-bordered table-striped mt-4">
    <thead>
        <tr>
            <th>Nombre</th>
            <th>Cliente</th>
            <th>Ubicacion</th>
            <th>Responsable</th>
        </tr>
    </thead>
    <tbody>
        {% for p in projects %}
        <tr>
            <td>{{ p.nombre }}</td>
            <td>{{ p.cliente }}</td>
            <td>{{ p.ubicacion }}</td>
            <td>{{ p.responsable }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>

{% endblock %}
'@ | Set-Content -Encoding UTF8 ".\templates\projects\list.html"

Write-Host "✔ templates/projects/list.html creado"

# 7. documents/list.html
@'
{% extends "base.html" %}
{% block content %}

<h2>Documentos</h2>

<table class="table table-bordered table-striped mt-4">
    <thead>
        <tr>
            <th>Nombre</th>
            <th>Proyecto</th>
            <th>Tipo</th>
            <th>Version</th>
            <th>Estado</th>
        </tr>
    </thead>
    <tbody>
        {% for d in documents %}
        <tr>
            <td>{{ d.nombre }}</td>
            <td>{{ d.proyecto }}</td>
            <td>{{ d.tipo }}</td>
            <td>{{ d.version }}</td>
            <td>{{ d.estado }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>

{% endblock %}
'@ | Set-Content -Encoding UTF8 ".\templates\documents\list.html"

Write-Host "✔ templates/documents/list.html creado"

# 8. chatbot/ui.html
@'
{% extends "base.html" %}
{% block content %}

<h2>Chatbot Inteligente</h2>

<form method="POST">
    {% csrf_token %}
    <textarea name="query" class="form-control" rows="4" placeholder="Escribe tu pregunta..."></textarea>
    <button class="btn btn-primary mt-3" type="submit">Enviar</button>
</form>

{% if answer %}
<div class="card mt-4 p-3">
    <h5>Respuesta:</h5>
    <p style="white-space: pre-line;">{{ answer }}</p>
</div>
{% endif %}

{% endblock %}
'@ | Set-Content -Encoding UTF8 ".\templates\chatbot\ui.html"

Write-Host "✔ templates/chatbot/ui.html creado"

# 9. views.py completo (home, login, proyectos, documentos, chatbot)
@'
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Usuario o contrasena incorrectos")
    return render(request, "auth/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def home(request):
    return render(request, "dashboard.html")

@login_required
def projects_view(request):
    try:
        resp = requests.get("http://127.0.0.1:8000/api/projects/")
        projects = resp.json()
    except Exception:
        projects = []
    return render(request, "projects/list.html", {"projects": projects})

@login_required
def documents_view(request):
    try:
        resp = requests.get("http://127.0.0.1:8000/api/documents/")
        documents = resp.json()
    except Exception:
        documents = []
    return render(request, "documents/list.html", {"documents": documents})

@login_required
def chatbot_ui(request):
    answer = None
    if request.method == "POST":
        q = request.POST.get("query")
        try:
            resp = requests.post(
                "http://127.0.0.1:8000/api/chatbot/query/",
                json={"query": q},
                timeout=40
            )
            data = resp.json()
            answer = data.get("answer", "")
        except Exception:
            answer = "Hubo un error al consultar el chatbot."
    return render(request, "chatbot/ui.html", {"answer": answer})
'@ | Set-Content -Encoding UTF8 $viewsPath

Write-Host "✔ views.py creado"

# 10. urls.py del proyecto
@'
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from sgd_geologia.views import (
    home,
    login_view,
    logout_view,
    projects_view,
    documents_view,
    chatbot_ui,
)

urlpatterns = [
    path("", home, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("projects/", projects_view, name="projects"),
    path("documents/", documents_view, name="documents"),
    path("chatbot_ui/", chatbot_ui, name="chatbot_ui"),

    path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
    path("api/projects/", include("projects.urls")),
    path("api/documents/", include("documents.urls")),
    path("api/chatbot/", include("chatbot.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'@ | Set-Content -Encoding UTF8 $urlsPath

Write-Host "✔ urls.py actualizado"

# 11. Asegurar LOGIN_URL en settings.py
if (Test-Path $settingsPath) {
    $settings = Get-Content $settingsPath
    if ($settings -notmatch "LOGIN_URL") {
        Add-Content -Encoding UTF8 $settingsPath "`nLOGIN_URL = '/login/'"
        Write-Host "✔ LOGIN_URL agregado a settings.py"
    } else {
        Write-Host "LOGIN_URL ya existe en settings.py"
    }
}

Write-Host ""
Write-Host "========================================="
Write-Host " UI completa generada."
Write-Host " Rutas:"
Write-Host "  - /login/"
Write-Host "  - /"
Write-Host "  - /projects/"
Write-Host "  - /documents/"
Write-Host "  - /chatbot_ui/"
Write-Host "========================================="
