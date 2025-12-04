from documents.models import Document
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
