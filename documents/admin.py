from django.contrib import admin
from .models import Document, DocumentMetadata

class DocumentMetadataInline(admin.TabularInline):
    model = DocumentMetadata
    extra = 0

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("nombre", "proyecto", "tipo", "estado", "version", "eliminado", "created_at")
    list_filter = ("estado", "tipo", "eliminado")
    search_fields = ("nombre", "proyecto__nombre")
    inlines = [DocumentMetadataInline]

@admin.register(DocumentMetadata)
class DocumentMetadataAdmin(admin.ModelAdmin):
    list_display = ("document", "clave", "valor")
    search_fields = ("document__nombre", "clave", "valor")
