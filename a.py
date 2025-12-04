import os
import sys

BASE = os.getcwd()

print("\n=== INICIANDO REPARACIÓN COMPLETA DEL SGD + CHATBOT ===\n")

# ------------------------------------------------------------
# Crear carpetas necesarias
# ------------------------------------------------------------
dirs_needed = [
    "templates/projects",
    "templates/documents",
    "chatbot",
]

for d in dirs_needed:
    path = os.path.join(BASE, d)
    os.makedirs(path, exist_ok=True)

print("✔ Carpetas necesarias verificadas/creadas.")


# ------------------------------------------------------------
# 1. REEMPLAZAR sgd_geologia/urls.py COMPLETO
# ------------------------------------------------------------
urls_main_path = os.path.join(BASE, "sgd_geologia", "urls.py")

urls_main_content = """from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from sgd_geologia.views import home, login_view, logout_view, projects_view, documents_view, chatbot_ui

urlpatterns = [

    # HOME Y LOGIN
    path("", home, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # FRONTEND HTML
    path("projects/", projects_view, name="projects"),
    path("documents/", documents_view, name="documents"),
    path("chatbot_ui/", chatbot_ui, name="chatbot_ui"),

    # API REST
    path("api/projects/", include("projects.api_urls")),
    path("api/documents/", include("documents.urls")),
    path("api/chatbot/", include("chatbot.api_urls")),
    path("api/accounts/", include("accounts.urls")),

    # ADMIN
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""

with open(urls_main_path, "w", encoding="utf-8") as f:
    f.write(urls_main_content)

print("✔ sgd_geologia/urls.py corregido.")


# ------------------------------------------------------------
# 2. REEMPLAZAR COMPLETAMENTE sgd_geologia/views.py
# ------------------------------------------------------------
views_main_path = os.path.join(BASE, "sgd_geologia", "views.py")

views_main_content = """from django.shortcuts import render, redirect
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
"""

with open(views_main_path, "w", encoding="utf-8") as f:
    f.write(views_main_content)

print("✔ Vistas principales reparadas.")


# ------------------------------------------------------------
# 3. CREAR TEMPLATES DE PROYECTOS Y DOCUMENTOS
# ------------------------------------------------------------

templates_projects_path = os.path.join(BASE, "templates/projects/list.html")
templates_documents_path = os.path.join(BASE, "templates/documents/list.html")

projects_template = """{% extends "base.html" %}
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
"""

with open(templates_projects_path, "w", encoding="utf-8") as f:
    f.write(projects_template)

print("✔ Template projects/list.html corregido.")


documents_template = """{% extends "base.html" %}
{% block content %}

<h2>Documentos</h2>

<table class="table table-striped">
    <thead>
        <tr>
            <th>Nombre</th>
            <th>Proyecto</th>
            <th>Tipo</th>
            <th>Estado</th>
            <th>Versión</th>
        </tr>
    </thead>
    <tbody>
        {% for d in documents %}
        <tr>
            <td>{{ d.nombre }}</td>
            <td>{{ d.proyecto.nombre }}</td>
            <td>{{ d.tipo }}</td>
            <td>{{ d.estado }}</td>
            <td>{{ d.version }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>

{% endblock %}
"""

with open(templates_documents_path, "w", encoding="utf-8") as f:
    f.write(documents_template)

print("✔ Template documents/list.html corregido.")


# ------------------------------------------------------------
# 4. CREAR ARQUITECTURA COMPLETA DEL CHATBOT
# ------------------------------------------------------------

chatbot_api_urls_path = os.path.join(BASE, "chatbot/api_urls.py")
chatbot_views_api_path = os.path.join(BASE, "chatbot/views_api.py")
chatbot_views_docs_path = os.path.join(BASE, "chatbot/views_docs.py")
chatbot_search_engine_path = os.path.join(BASE, "chatbot/search_engine.py")
chatbot_report_path = os.path.join(BASE, "chatbot/views_report.py")
chatbot_doc_assistant_path = os.path.join(BASE, "chatbot/doc_assistant.py")

# ========== api_urls.py ==========
with open(chatbot_api_urls_path, "w", encoding="utf-8") as f:
    f.write("""from django.urls import path
from .views_api import chatbot_api
from .views_docs import chatbot_doc_api
from .views_search import chatbot_search_api
from .views_report import chatbot_doc_report

urlpatterns = [
    path("", chatbot_api, name="chatbot_api"),
    path("documents/", chatbot_doc_api, name="chatbot_doc_api"),
    path("search/", chatbot_search_api, name="chatbot_search_api"),
    path("documents/report/", chatbot_doc_report, name="chatbot_doc_report"),
]
""")

print("✔ chatbot/api_urls.py creado.")


# ========== views_api.py ==========
with open(chatbot_views_api_path, "w", encoding="utf-8") as f:
    f.write("""import os
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .search_engine import buscar_documentos

OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

@csrf_exempt
def chatbot_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    body = json.loads(request.body)
    prompt = body.get("prompt", "").strip()

    # Detectar si es consulta de búsqueda
    posibles = ["buscar", "busca", "proyecto", "documentos", "listame"]

    if any(p in prompt.lower() for p in posibles):
        docs = buscar_documentos(prompt)
        lista = [f"- ({d.id}) {d.nombre} — {d.proyecto.nombre}" for d in docs]
        resumen = "\\n".join(lista) if lista else "No se encontraron documentos."

        payload = {
            "model": "qwen/qwen-2.5-7b-instruct",
            "messages": [
                {"role": "system", "content": "Sos un asistente documental experto."},
                {"role": "user", "content": f"El usuario dijo: '{prompt}'.\\nDocumentos encontrados:\\n{resumen}\\nGenerá una respuesta clara."}
            ]
        }

        r = requests.post(API_URL, json=payload,
            headers={"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"})
        data = r.json()
        return JsonResponse({"response": data["choices"][0]["message"]["content"]})

    # Conversación normal
    payload = {
        "model": "qwen/qwen-2.5-7b-instruct",
        "messages": [
            {"role": "system", "content": "Sos un asistente de documentación técnica."},
            {"role": "user", "content": prompt}
        ]
    }

    r = requests.post(API_URL, json=payload,
        headers={"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"})
    data = r.json()

    return JsonResponse({"response": data["choices"][0]["message"]["content"]})
""")

print("✔ chatbot/views_api.py creado.")


# ========== search_engine.py ==========
with open(chatbot_search_engine_path, "w", encoding="utf-8") as f:
    f.write("""from documents.models import Document
from django.db.models import Q
from .doc_assistant import leer_pdf
import os

def buscar_documentos(query):
    qs = Document.objects.filter(eliminado=False)

    if not query:
        return qs[:20]

    base = qs.filter(
        Q(nombre__icontains=query) |
        Q(descripcion__icontains=query) |
        Q(tipo__icontains=query) |
        Q(estado__icontains=query) |
        Q(proyecto__nombre__icontains=query)
    )

    resultados = list(base)

    extras = []
    for d in qs.exclude(id__in=[x.id for x in resultados])[:20]:
        ext = os.path.splitext(d.archivo.name)[1].lower()
        if ext == ".pdf":
            try:
                texto = leer_pdf(d.archivo.path)
                if query.lower() in (texto or "").lower():
                    extras.append(d)
            except Exception:
                pass

    return (resultados + extras)[:20]
""")

print("✔ chatbot/search_engine.py creado.")


# ========== views_docs.py ==========
with open(chatbot_views_docs_path, "w", encoding="utf-8") as f:
    f.write("""import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from documents.models import Document
from .doc_assistant import (
    leer_contenido_generico,
    tarea_resumen,
    tarea_cumplimiento_ens,
    tarea_clasificacion,
    tarea_recomendaciones,
)

@csrf_exempt
def chatbot_doc_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    data = json.loads(request.body)

    doc_id = data.get("document_id")
    prompt = data.get("prompt", "").strip()
    task = (data.get("task") or "").lower()

    if not doc_id:
        return JsonResponse({"error": "Falta document_id"}, status=400)

    try:
        doc = Document.objects.get(id=doc_id)
    except:
        return JsonResponse({"error": "Documento no encontrado"}, status=404)

    contenido = leer_contenido_generico(doc.archivo.path, doc.tipo, doc.nombre)

    if task == "ens":
        respuesta = tarea_cumplimiento_ens(contenido)
    elif task == "clasificacion":
        respuesta = tarea_clasificacion(contenido)
    elif task == "recomendaciones":
        respuesta = tarea_recomendaciones(contenido)
    else:
        respuesta = tarea_resumen(contenido, contexto_extra=prompt)

    return JsonResponse({
        "document_id": doc_id,
        "document_name": doc.nombre,
        "task": task or "resumen",
        "response": respuesta
    })
""")

print("✔ chatbot/views_docs.py creado.")


# ========== views_report.py ==========
with open(chatbot_report_path, "w", encoding="utf-8") as f:
    f.write("""import io
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from documents.models import Document
from .doc_assistant import (
    leer_contenido_generico,
    tarea_resumen,
    tarea_cumplimiento_ens,
    tarea_clasificacion,
    tarea_recomendaciones,
)

@csrf_exempt
def chatbot_doc_report(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    data = json.loads(request.body)
    doc_id = data.get("document_id")

    if not doc_id:
        return JsonResponse({"error": "Falta document_id"}, status=400)

    try:
        doc = Document.objects.get(id=doc_id)
    except:
        return JsonResponse({"error": "Documento no encontrado"}, status=404)

    contenido = leer_contenido_generico(doc.archivo.path, doc.tipo, doc.nombre)

    resumen = tarea_resumen(contenido)
    ens = tarea_cumplimiento_ens(contenido)
    clas = tarea_clasificacion(contenido)
    recom = tarea_recomendaciones(contenido)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    def write(title, text):
        nonlocal y
        p.setFont("Helvetica-Bold", 12)
        p.drawString(40, y, title)
        y -= 20
        p.setFont("Helvetica", 10)
        for line in text.splitlines():
            if y < 60:
                p.showPage()
                y = height - 50
                p.setFont("Helvetica", 10)
            p.drawString(40, y, line[:120])
            y -= 14
        y -= 10

    write("1. Resumen", resumen)
    write("2. Cumplimiento ENS", ens)
    write("3. Clasificación", clas)
    write("4. Recomendaciones", recom)

    p.showPage()
    p.save()
    buffer.seek(0)

    resp = HttpResponse(buffer, content_type="application/pdf")
    resp["Content-Disposition"] = f'attachment; filename="informe_ia_doc_{doc.id}.pdf"'
    return resp
""")

print("✔ chatbot/views_report.py creado.")


# ========== doc_assistant.py ==========
with open(chatbot_doc_assistant_path, "w", encoding="utf-8") as f:
    f.write("""import os
import requests
from PyPDF2 import PdfReader
from docx import Document as DocxDocument

OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"


def leer_pdf(ruta):
    texto = ""
    with open(ruta, "rb") as f:
        pdf = PdfReader(f)
        for page in pdf.pages:
            t = page.extract_text() or ""
            texto += t + "\\n"
    return texto.strip()


def leer_docx(ruta):
    doc = DocxDocument(ruta)
    return "\\n".join(p.text for p in doc.paragraphs)


def leer_txt(ruta):
    with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def leer_contenido_generico(ruta, mime_type, nombre_archivo=""):
    ext = os.path.splitext(nombre_archivo)[1].lower()

    if ext == ".pdf":
        return leer_pdf(ruta)
    if ext == ".docx":
        return leer_docx(ruta)
    if ext in [".txt", ".log", ".csv"]:
        return leer_txt(ruta)

    return f"[Formato no soportado] {nombre_archivo}"


def llamar_openrouter(messages):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"model": "qwen/qwen-2.5-7b-instruct", "messages": messages}
    r = requests.post(API_URL, json=payload, headers=headers)
    data = r.json()
    return data["choices"][0]["message"]["content"]


def tarea_resumen(contenido, contexto_extra=""):
    mensajes = [
        {"role": "system", "content": "Sos un asistente experto en documentos técnicos."},
        {"role": "user", "content": f"{contexto_extra}\\n\\nResumí este documento:\\n{contenido}"},
    ]
    return llamar_openrouter(mensajes)


def tarea_cumplimiento_ens(contenido):
    mensajes = [
        {"role": "system", "content": "Experto en ENS / ISO 27001."},
        {"role": "user", "content": f"Analizá cumplimiento ENS / ISO:\\n{contenido}"},
    ]
    return llamar_openrouter(mensajes)


def tarea_clasificacion(contenido):
    mensajes = [
        {"role": "system", "content": "Especialista en gestión documental."},
        {"role": "user", "content": f"Clasifica este documento:\\n{contenido}"},
    ]
    return llamar_openrouter(mensajes)


def tarea_recomendaciones(contenido):
    mensajes = [
        {"role": "system", "content": "Consultor técnico senior."},
        {"role": "user", "content": f"Recomendaciones para mejorar:\\n{contenido}"},
    ]
    return llamar_openrouter(mensajes)
""")

print("✔ chatbot/doc_assistant.py creado.")

print("\n=== ✔ REPARACIÓN COMPLETA FINALIZADA ===")
print("Ahora ejecutá: python manage.py runserver")
print("Abrí:")
print("  - http://localhost:8000/")
print("  - http://localhost:8000/projects/")
print("  - http://localhost:8000/documents/")
print("  - http://localhost:8000/chatbot_ui/")
print("\nChatbot inteligente listo con:")
print("  - Lectura PDF / DOCX / TXT")
print("  - Búsqueda inteligente")
print("  - Análisis ENS / ISO")
print("  - Clasificación")
print("  - Recomendaciones")
print("  - Generación de informe PDF\n")
