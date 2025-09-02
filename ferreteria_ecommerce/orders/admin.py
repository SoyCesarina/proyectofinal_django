from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total']
    fields = ['product', 'variant', 'quantity', 'price', 'total']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_name', 'status', 'total', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'customer_name', 'customer_email']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Información de la Orden', {
            'fields': ('order_number', 'status', 'session')
        }),
        ('Información del Cliente', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Dirección de Envío', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_state', 'shipping_zip_code')
        }),
        ('Información de Pago', {
            'fields': ('subtotal', 'discount', 'total', 'coupon')
        }),
        ('Notas', {
            'fields': ('notes',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'variant_display', 'quantity', 'price', 'total']
    list_filter = ['order__status', 'product__category']
    search_fields = ['order__order_number', 'product__name', 'variant__name', 'variant__value']
    readonly_fields = ['total']

    def variant_display(self, obj):
        """Mostrar información de la variante"""
        if obj.variant:
            return f"{obj.variant.name}: {obj.variant.value}"
        return "Sin variante"
    variant_display.short_description = 'Variante'
