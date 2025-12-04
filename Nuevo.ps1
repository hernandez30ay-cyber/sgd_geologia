Write-Host "=== Corrigiendo estructura ===" -ForegroundColor Cyan

# Rutas
$projDir = "projects"
$tmplDir = "templates/projects"

# Crear folders si no existen
if (!(Test-Path $projDir)) { mkdir $projDir }
if (!(Test-Path $tmplDir)) { mkdir $tmplDir }

# -------------------------------------------
# 1. Crear projects/api_urls.py
# -------------------------------------------

"from rest_framework.routers import DefaultRouter"            | Set-Content "$projDir/api_urls.py"
"from .views import ProjectViewSet"                          | Add-Content "$projDir/api_urls.py"
""                                                           | Add-Content "$projDir/api_urls.py"
"router = DefaultRouter()"                                   | Add-Content "$projDir/api_urls.py"
"router.register(r\"\", ProjectViewSet, basename=\"projects\")" | Add-Content "$projDir/api_urls.py"
""                                                           | Add-Content "$projDir/api_urls.py"
"urlpatterns = router.urls"                                  | Add-Content "$projDir/api_urls.py"

Write-Host "✔ api_urls.py creado" -ForegroundColor Green

# -------------------------------------------
# 2. Crear projects/views_html.py
# -------------------------------------------

"from django.shortcuts import render"                        | Set-Content "$projDir/views_html.py"
"from django.contrib.auth.decorators import login_required" | Add-Content "$projDir/views_html.py"
"from .models import Project"                               | Add-Content "$projDir/views_html.py"
""                                                           | Add-Content "$projDir/views_html.py"
"@login_required"                                            | Add-Content "$projDir/views_html.py"
"def project_list(request):"                                 | Add-Content "$projDir/views_html.py"
"    proyectos = Project.objects.all()"                      | Add-Content "$projDir/views_html.py"
"    return render(request, \"projects/list.html\", {\"proyectos\": proyectos})" | Add-Content "$projDir/views_html.py"

Write-Host "✔ views_html.py creado" -ForegroundColor Green

# -------------------------------------------
# 3. Crear projects/urls.py
# -------------------------------------------

"from django.urls import path"                               | Set-Content "$projDir/urls.py"
"from .views_html import project_list"                       | Add-Content "$projDir/urls.py"
""                                                           | Add-Content "$projDir/urls.py"
"urlpatterns = ["                                            | Add-Content "$projDir/urls.py"
"    path('', project_list, name='project_list'),"           | Add-Content "$projDir/urls.py"
"]"                                                          | Add-Content "$projDir/urls.py"

Write-Host "✔ urls.py creado" -ForegroundColor Green

# -------------------------------------------
# 4. Crear template
# -------------------------------------------

"{% extends ""base.html"" %}"                                | Set-Content "$tmplDir/list.html"
"{% block content %}"                                        | Add-Content "$tmplDir/list.html"
""                                                           | Add-Content "$tmplDir/list.html"
"<h2>Proyectos</h2>"                                         | Add-Content "$tmplDir/list.html"
""                                                           | Add-Content "$tmplDir/list.html"
"<table class='table table-striped'>"                        | Add-Content "$tmplDir/list.html"
"  <thead>"                                                  | Add-Content "$tmplDir/list.html"
"    <tr><th>Nombre</th><th>Cliente</th><th>Ubicación</th><th>Responsable</th></tr>" | Add-Content "$tmplDir/list.html"
"  </thead>"                                                 | Add-Content "$tmplDir/list.html"
"  <tbody>"                                                  | Add-Content "$tmplDir/list.html"
"    {% for p in proyectos %}"                               | Add-Content "$tmplDir/list.html"
"    <tr>"                                                   | Add-Content "$tmplDir/list.html"
"      <td>{{ p.nombre }}</td>"                              | Add-Content "$tmplDir/list.html"
"      <td>{{ p.cliente }}</td>"                             | Add-Content "$tmplDir/list.html"
"      <td>{{ p.ubicacion }}</td>"                           | Add-Content "$tmplDir/list.html"
"      <td>{{ p.responsable }}</td>"                         | Add-Content "$tmplDir/list.html"
"    </tr>"                                                  | Add-Content "$tmplDir/list.html"
"    {% endfor %}"                                           | Add-Content "$tmplDir/list.html"
"  </tbody>"                                                 | Add-Content "$tmplDir/list.html"
"</table>"                                                   | Add-Content "$tmplDir/list.html"
""                                                           | Add-Content "$tmplDir/list.html"
"{% endblock %}"                                             | Add-Content "$tmplDir/list.html"

Write-Host "✔ Template list.html creado" -ForegroundColor Green

# -------------------------------------------
# 5. Editar sgd_geologia/urls.py
# -------------------------------------------

$mainUrls = "sgd_geologia/urls.py"
$lines = Get-Content $mainUrls

# Eliminar duplicados previos
$lines = $lines | Where-Object { $_ -notmatch "projects.urls" -and $_ -notmatch "projects.api_urls" }

# Insertar rutas HTML + API
$insert = @(
'    path("projects/", include("projects.urls")),',
'    path("api/projects/", include("projects.api_urls")),'
)

# Insertar después de urlpatterns = [
$newContent = @()

foreach ($line in $lines) {
    $newContent += $line
    if ($line -match "urlpatterns = \[") {
        $newContent += $insert
    }
}

$newContent | Set-Content $mainUrls -Encoding UTF8

Write-Host "✔ sgd_geologia/urls.py modificado" -ForegroundColor Green

Write-Host "`n=== TODO LISTO ===" -ForegroundColor Cyan
Write-Host "Inicia Django con: python manage.py runserver" -ForegroundColor Yellow
Write-Host "Abrí: http://localhost:8000/projects/" -ForegroundColor Green
