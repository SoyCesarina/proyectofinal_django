from django.db import models
from django.contrib.sessions.models import Session
from catalog.models import Product, ProductVariant
from promotions.models import Coupon


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmada'),
        ('ready_to_ship', 'Lista para despachar'),
        ('shipped', 'Despachada'),
        ('delivered', 'Entregada'),
        ('cancelled', 'Cancelada'),
    ]

    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name="Sesión")
    order_number = models.CharField(max_length=20, unique=True, verbose_name="Número de orden")
    customer_name = models.CharField(max_length=200, verbose_name="Nombre del cliente")
    customer_email = models.EmailField(verbose_name="Email del cliente")
    customer_phone = models.CharField(max_length=20, verbose_name="Teléfono del cliente")
    shipping_address = models.TextField(verbose_name="Dirección de envío")
    shipping_city = models.CharField(max_length=100, verbose_name="Ciudad")
    shipping_state = models.CharField(max_length=100, verbose_name="Estado/Provincia")
    shipping_zip_code = models.CharField(max_length=20, verbose_name="Código postal")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Estado")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal")
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Descuento")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total")
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cupón")
    notes = models.TextField(blank=True, verbose_name="Notas")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Orden"
        verbose_name_plural = "Órdenes"
        ordering = ['-created_at']

    def __str__(self):
        return f"Orden {self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            import uuid
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('orders:order_detail', kwargs={'order_number': self.order_number})


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Orden")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Variante")
    quantity = models.PositiveIntegerField(verbose_name="Cantidad")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio unitario")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total")

    class Meta:
        verbose_name = "Item de orden"
        verbose_name_plural = "Items de orden"

    def __str__(self):
        if self.variant:
            return f"{self.quantity}x {self.product.name} - {self.variant.name}: {self.variant.value}"
        return f"{self.quantity}x {self.product.name}"

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        super().save(*args, **kwargs)

    def get_product_display_name(self):
        """Obtener nombre completo del producto con variante"""
        if self.variant:
            return f"{self.product.name} - {self.variant.name}: {self.variant.value}"
        return self.product.name

    def get_sku(self):
        """Obtener SKU del producto o variante"""
        if self.variant:
            return self.variant.sku
        return self.product.sku
