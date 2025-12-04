from django.conf import settings
from documents.search import search_documents

# Esta funciÃ³n estarÃ­a lista para usar OpenRoute realmente.
# AquÃ­ dejamos un flujo simplificado que busca directamente en los documentos.
def process_user_query(query: str):
    docs = search_documents(query=query)
    results = []
    for d in docs[:10]:
        results.append(
            {
                "id": d.id,
                "nombre": d.nombre,
                "proyecto": d.proyecto.nombre,
                "tipo": d.tipo,
                "estado": d.estado,
                "version": d.version,
            }
        )

    if not results:
        respuesta = "No encontrÃ© documentos que coincidan con tu bÃºsqueda."
    else:
        respuesta = "EncontrÃ© los siguientes documentos:\n"
        for r in results:
            respuesta += f"- {r['nombre']} (Proyecto: {r['proyecto']}, v{r['version']})\n"

    return {
        "answer": respuesta,
        "documents": results,
    }
