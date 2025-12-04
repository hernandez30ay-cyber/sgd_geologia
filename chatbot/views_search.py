import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .search_engine import buscar_documentos

@csrf_exempt
def chatbot_search_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    data = json.loads(request.body)
    query = data.get("query", "").strip()

    resultados = buscar_documentos(query)

    lista = []
    for d in resultados:
        lista.append({
            "id": d.id,
            "nombre": d.nombre,
            "proyecto": d.proyecto.nombre,
            "estado": d.estado,
            "tipo": d.tipo,
        })

    return JsonResponse({"resultados": lista})
