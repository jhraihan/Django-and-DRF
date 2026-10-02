from django.contrib import admin
from .models import Service, Product


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'service_type', 'is_active', 'created_at')
    list_filter = ('service_type', 'is_active')
    search_fields = ('name',)
    list_editable = ('is_active',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'is_available', 'created_at')
    list_filter = ('is_available',)
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'is_available')
