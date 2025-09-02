from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Coupon(models.Model):
    DISCOUNT_TYPES = [
        ('percentage', 'Porcentaje'),
        ('fixed', 'Monto fijo'),
    ]

    code = models.CharField(max_length=20, unique=True, verbose_name="Código")
    description = models.CharField(max_length=200, blank=True, verbose_name="Descripción")
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES, default='percentage', verbose_name="Tipo de descuento")
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor del descuento")
    min_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Monto mínimo")
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Descuento máximo")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    valid_from = models.DateTimeField(verbose_name="Válido desde")
    valid_to = models.DateTimeField(verbose_name="Válido hasta")
    usage_limit = models.PositiveIntegerField(null=True, blank=True, verbose_name="Límite de uso")
    used_count = models.PositiveIntegerField(default=0, verbose_name="Veces usado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Cupón"
        verbose_name_plural = "Cupones"
        ordering = ['-created_at']

    def __str__(self):
        return self.code

    def is_valid(self):
        from django.utils import timezone
        from datetime import datetime
        
        now = datetime.now()
        
        # Verificar que el cupón esté activo
        if not self.is_active:
            return False
            
        # Verificar que esté dentro del rango de fechas válidas
        if not (self.valid_from <= now <= self.valid_to):
            return False
            
        # Verificar el límite de uso
        if self.usage_limit is not None and self.used_count >= self.usage_limit:
            return False
            
        return True

    def calculate_discount(self, total_amount):
        if not self.is_valid() or total_amount < self.min_amount:
            return Decimal('0.00')

        if self.discount_type == 'percentage':
            discount = (total_amount * self.discount_value) / 100
            if self.max_discount:
                discount = min(discount, self.max_discount)
        else:
            discount = self.discount_value

        return min(discount, total_amount)

    def use(self):
        if self.is_valid():
            self.used_count += 1
            self.save()
            return True
        return False
