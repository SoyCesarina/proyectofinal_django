from django.db import models
from catalog.models import Product, ProductVariant
from orders.models import Order


class InventoryMovement(models.Model):
    MOVEMENT_TYPES = [
        ('in', 'Entrada'),
        ('out', 'Salida'),
        ('adjustment', 'Ajuste'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Variante")
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES, verbose_name="Tipo de movimiento")
    quantity = models.IntegerField(verbose_name="Cantidad")
    reason = models.CharField(max_length=200, verbose_name="Motivo")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Orden relacionada")
    notes = models.TextField(blank=True, verbose_name="Notas")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Movimiento de inventario"
        verbose_name_plural = "Movimientos de inventario"
        ordering = ['-created_at']

    def __str__(self):
        variant_info = f" - {self.variant.name}: {self.variant.value}" if self.variant else ""
        return f"{self.get_movement_type_display()} - {self.product.name}{variant_info} ({self.quantity})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Actualizar stock del ItemStock correspondiente
        try:
            if self.variant:
                stock_item = self.product.stock_items.get(variant=self.variant)
            else:
                stock_item = self.product.stock_items.get(variant__isnull=True)
            
            if self.movement_type == 'in':
                stock_item.add_stock(self.quantity)
            elif self.movement_type == 'out':
                stock_item.consume_stock(self.quantity)
            elif self.movement_type == 'adjustment':
                # Para ajustes, establecer la cantidad directamente
                stock_item.quantity = self.quantity
                stock_item.save()
                
        except Exception as e:
            # Si hay error, solo registrar el movimiento sin afectar stock
            pass


class Shipment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Orden")
    tracking_number = models.CharField(max_length=100, blank=True, verbose_name="Número de seguimiento")
    carrier = models.CharField(max_length=100, blank=True, verbose_name="Transportista")
    shipped_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de despacho")
    notes = models.TextField(blank=True, verbose_name="Notas")

    class Meta:
        verbose_name = "Despacho"
        verbose_name_plural = "Despachos"
        ordering = ['-shipped_at']

    def __str__(self):
        return f"Despacho {self.order.order_number}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            # Marcar orden como despachada
            self.order.status = 'shipped'
            self.order.save()
            
            # Crear movimientos de inventario para cada item con variantes
            for item in self.order.items.all():
                InventoryMovement.objects.create(
                    product=item.product,
                    variant=item.variant,  # Incluir variante
                    movement_type='out',
                    quantity=item.quantity,
                    reason=f'Despacho orden {self.order.order_number}',
                    order=self.order
                )
