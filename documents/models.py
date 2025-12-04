from django.db import models
from django.contrib.auth.models import User
from projects.models import Project

class Document(models.Model):
    ESTADOS = [
        ("BORRADOR", "Borrador"),
        ("REVISION", "En revisiÃ³n"),
        ("APROBADO", "Aprobado"),
        ("ARCHIVADO", "Archivado"),
    ]

    proyecto = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="documentos")
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to="documentos/")
    tipo = models.CharField(max_length=50, blank=True)  # PDF, DWG, JPG, etc.
    version = models.IntegerField(default=1)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="BORRADOR")
    descripcion = models.TextField(blank=True)

    creado_por = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="documentos_creados"
    )
    actualizado_por = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="documentos_actualizados"
    )

    bloqueado_por = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="documentos_bloqueados"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    eliminado = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.nombre} (v{self.version})"


class DocumentMetadata(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="metadatos")
    clave = models.CharField(max_length=100)
    valor = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.document.nombre} | {self.clave} = {self.valor}"
