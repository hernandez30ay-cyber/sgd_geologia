from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("nombre", "cliente", "ubicacion", "responsable", "activo", "created_at")
    search_fields = ("nombre", "cliente", "ubicacion")
    list_filter = ("activo",)
