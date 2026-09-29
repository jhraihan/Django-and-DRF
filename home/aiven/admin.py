from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'service_type', 'is_active', 'created_at')
    list_filter = ('service_type', 'is_active')
    search_fields = ('name',)
    list_editable = ('is_active',)
