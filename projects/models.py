from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    nombre = models.CharField(max_length=255)
    cliente = models.CharField(max_length=255)
    ubicacion = models.CharField(max_length=255, blank=True)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    responsable = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="proyectos_responsable"
    )
    activo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.nombre
