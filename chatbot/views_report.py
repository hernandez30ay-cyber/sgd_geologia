import io
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
