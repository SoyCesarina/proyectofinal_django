from django.db import models
from django.contrib.sessions.models import Session
from catalog.models import Product, ProductVariant


class Cart(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name="Sesión")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"

    def __str__(self):
        return f"Carrito {self.id} - {self.session.session_key}"

    def get_total(self):
        return sum(item.get_total() for item in self.items.all())

    def get_item_count(self):
        return sum(item.quantity for item in self.items.all())

    def clear(self):
        self.items.all().delete()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="Carrito")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Variante")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio unitario")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Item del carrito"
        verbose_name_plural = "Items del carrito"
        unique_together = ['cart', 'product', 'variant']
        ordering = ['created_at']

    def __str__(self):
        if self.variant:
            return f"{self.quantity}x {self.product.name} - {self.variant.name}: {self.variant.value}"
        return f"{self.quantity}x {self.product.name}"

    def get_total(self):
        return self.quantity * self.price

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

    def save(self, *args, **kwargs):
        if not self.price:
            if self.variant:
                self.price = self.variant.get_final_price()
            else:
                self.price = self.product.price
        super().save(*args, **kwargs)
