from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Document, DocumentMetadata
from .serializers import DocumentSerializer, DocumentMetadataSerializer
from .search import search_documents
from projects.models import Project


class IsProjectMemberOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.filter(eliminado=False)
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectMemberOrAdmin]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(creado_por=user, actualizado_por=user)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(actualizado_por=user)

    # ===========================
    # BÚSQUEDA
    # ===========================
    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request):
        query = request.query_params.get("q")
        proyecto_id = request.query_params.get("proyecto_id")
        tipo = request.query_params.get("tipo")
        estado = request.query_params.get("estado")

        qs = search_documents(query=query, proyecto_id=proyecto_id, tipo=tipo, estado=estado)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    # ===========================
    # CHECKOUT
    # ===========================
    @action(detail=True, methods=["post"], url_path="checkout")
    def checkout(self, request, pk=None):
        doc = self.get_object()
        if doc.bloqueado_por and doc.bloqueado_por != request.user:
            return Response({"detail": "Documento ya está bloqueado."}, status=400)
        doc.bloqueado_por = request.user
        doc.save()
        return Response({"detail": "Documento bloqueado para edición."})

    # ===========================
    # CHECKIN
    # ===========================
    @action(detail=True, methods=["post"], url_path="checkin")
    def checkin(self, request, pk=None):
        doc = self.get_object()
        if doc.bloqueado_por != request.user:
            return Response({"detail": "No sos quien tiene el bloqueo."}, status=400)
        doc.bloqueado_por = None
        doc.save()
        return Response({"detail": "Documento desbloqueado."})

    # ===========================
    # PAPELERA
    # ===========================
    @action(detail=True, methods=["delete"], url_path="trash")
    def send_to_trash(self, request, pk=None):
        doc = self.get_object()
        doc.eliminado = True
        doc.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # ===========================
    # SUBIDA DE UN SOLO ARCHIVO
    # ===========================
    @action(detail=False, methods=["post"], url_path="upload")
    def upload(self, request):
        archivo = request.FILES.get("archivo")
        proyecto_id = request.data.get("proyecto_id")
        descripcion = request.data.get("descripcion", "")

        if not archivo:
            return Response({"detail": "No se recibió archivo."}, status=400)

        if not proyecto_id:
            return Response({"detail": "Falta proyecto_id."}, status=400)

        try:
            proyecto = Project.objects.get(id=proyecto_id)
        except Project.DoesNotExist:
            return Response({"detail": "Proyecto no encontrado."}, status=404)

        doc = Document.objects.create(
            proyecto=proyecto,
            archivo=archivo,
            nombre=archivo.name,
            descripcion=descripcion,
            tipo=archivo.content_type,
            creado_por=request.user,
            actualizado_por=request.user,
        )

        serializer = self.get_serializer(doc)
        return Response(serializer.data, status=201)

    # ===========================
    # SUBIDA MÚLTIPLE
    # ===========================
    @action(detail=False, methods=["post"], url_path="upload-multiple")
    def upload_multiple(self, request):
        archivos = request.FILES.getlist("archivos")
        proyecto_id = request.data.get("proyecto_id")

        if not archivos:
            return Response({"detail": "No se recibieron archivos."}, status=400)

        if not proyecto_id:
            return Response({"detail": "Falta proyecto_id."}, status=400)

        try:
            proyecto = Project.objects.get(id=proyecto_id)
        except Project.DoesNotExist:
            return Response({"detail": "Proyecto no encontrado."}, status=404)

        documentos_creados = []

        for file in archivos:
            doc = Document.objects.create(
                proyecto=proyecto,
                archivo=file,
                nombre=file.name,
                tipo=file.content_type,
                creado_por=request.user,
                actualizado_por=request.user,
            )
            documentos_creados.append(self.get_serializer(doc).data)

        return Response({"creados": documentos_creados}, status=201)


# ===================================================
# METADATOS
# ===================================================
class DocumentMetadataViewSet(viewsets.ModelViewSet):
    queryset = DocumentMetadata.objects.all()
    serializer_class = DocumentMetadataSerializer
    permission_classes = [permissions.IsAuthenticated]
