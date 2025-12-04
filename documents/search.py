from django.db.models import Q
from .models import Document

def search_documents(query=None, proyecto_id=None, tipo=None, estado=None):
    qs = Document.objects.filter(eliminado=False)

    if proyecto_id:
        qs = qs.filter(proyecto_id=proyecto_id)

    if tipo:
        qs = qs.filter(tipo__iexact=tipo)

    if estado:
        qs = qs.filter(estado=estado)

    if query:
        qs = qs.filter(
            Q(nombre__icontains=query)
            | Q(descripcion__icontains=query)
            | Q(metadatos__valor__icontains=query)
        ).distinct()

    return qs
