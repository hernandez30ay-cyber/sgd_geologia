from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("user", "path", "method", "status_code", "ip_address", "created_at")
    search_fields = ("user__username", "path", "ip_address")
    list_filter = ("method", "status_code")
