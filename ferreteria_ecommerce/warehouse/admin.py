from django.contrib import admin
from .models import InventoryMovement, Shipment


@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'variant_display', 'movement_type', 'quantity', 'reason', 'order', 'created_at']
    list_filter = ['movement_type', 'created_at', 'product__category']
    search_fields = ['product__name', 'variant__name', 'variant__value', 'reason', 'order__order_number']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Producto y Variante', {
            'fields': ('product', 'variant')
        }),
        ('Movimiento', {
            'fields': ('movement_type', 'quantity', 'reason')
        }),
        ('Orden Relacionada', {
            'fields': ('order', 'notes')
        }),
        ('Fechas', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def variant_display(self, obj):
        """Mostrar información de la variante"""
        if obj.variant:
            return f"{obj.variant.name}: {obj.variant.value}"
        return "Sin variante"
    variant_display.short_description = 'Variante'


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['order', 'tracking_number', 'carrier', 'shipped_at']
    list_filter = ['shipped_at', 'carrier']
    search_fields = ['order__order_number', 'tracking_number']
    readonly_fields = ['shipped_at']
