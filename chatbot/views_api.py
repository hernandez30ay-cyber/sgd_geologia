import os
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
        resumen = "\n".join(lista) if lista else "No se encontraron documentos."

        payload = {
            "model": "qwen/qwen-2.5-7b-instruct",
            "messages": [
                {"role": "system", "content": "Sos un asistente documental experto."},
                {"role": "user", "content": f"El usuario dijo: '{prompt}'.\nDocumentos encontrados:\n{resumen}\nGenerá una respuesta clara."}
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
