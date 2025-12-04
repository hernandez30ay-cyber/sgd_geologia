Write-Host "=== Arreglando estructura de rutas de 'projects' ===" -ForegroundColor Cyan

$projectsDir = "projects"
$templatesDir = "templates/projects"

# 1. Crear api_urls.py
$apiUrlsPath = "$projectsDir/api_urls.py"
@"
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet

router = DefaultRouter()
router.register(r"", ProjectViewSet, basename="projects")

urlpatterns = router.urls
"@ | Out-File $apiUrlsPath -Encoding utf8
Write-Host "✔ Creado: projects/api_urls.py" -ForegroundColor Green

# 2. Crear views_html.py
$viewsHtmlPath = "$projectsDir/views_html.py"
@"
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Project

@login_required
def project_list(request):
    proyectos = Project.objects.all()
    return render(request, "projects/list.html", {"proyectos": proyectos})
"@ | Out-File $viewsHtmlPath -Encoding utf8
Write-Host "✔ Creado: projects/views_html.py" -ForegroundColor Green

# 3. Crear urls.py (HTML)
$urlsPath = "$projectsDir/urls.py"
@"
from django.urls import path
from .views_html import project_list

urlpatterns = [
    path('', project_list, name='project_list'),
]
"@ | Out-File $urlsPath -Encoding utf8
Write-Host "✔ Creado: projects/urls.py (HTML)" -ForegroundColor Green

# 4. Crear template projects/list.html si no existe
if (!(Test-Path $templatesDir)) {
    New-Item -ItemType Directory -Path $templatesDir | Out-Null
    Write-Host "✔ Carpeta creada: templates/projects" -ForegroundColor Yellow
}

$templateFile = "$templatesDir/list.html"
@"
{% extends "base.html" %}
{% block content %}

<h2>Proyectos</h2>

<table class="table table-striped">
    <thead>
        <tr>
            <th>Nombre</th>
            <th>Cliente</th>
            <th>Ubicación</th>
            <th>Responsable</th>
        </tr>
    </thead>
    <tbody>
        {% for p in proyectos %}
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
"@ | Out-File $templateFile -Encoding utf8
Write-Host "✔ Template actualizado: templates/projects/list.html" -ForegroundColor Green

# 5. Modificar sgd_geologia/urls.py
$mainUrls = "sgd_geologia/urls.py"

$urlsContent = Get-Content $mainUrls -Raw

# Elimina cualquier "include('projects.urls')" duplicado o router que use /projects/
$urlsContent = $urlsContent -replace ".*projects\.urls.*", ""

# Añadir rutas limpias para API y HTML
$newRoutes = @"
    path("projects/", include("projects.urls")),          # HTML
    path("api/projects/", include("projects.api_urls")),  # API
"@

# Insertar después de la primera línea urlpatterns = [
$urlsContent = $urlsContent -replace "urlpatterns = \[", "urlpatterns = [`r`n$newRoutes"

$urlsContent | Out-File $mainUrls -Encoding utf8
Write-Host "✔ Modificado: sgd_geologia/urls.py (separadas rutas HTML y API)" -ForegroundColor Green

Write-Host "`n=== TODO LISTO ===" -ForegroundColor Green
Write-Host "Ahora ejecuta:" -ForegroundColor Yellow
Write-Host "  python manage.py runserver" -ForegroundColor Yellow
Write-Host "Y abre http://localhost:8000/projects/" -ForegroundColor Cyan
Write-Host "Deberías ver tus 20 proyectos inmediatamente." -ForegroundColor Green
