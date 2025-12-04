import json
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
