from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import base64


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name="Categoría padre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Imagen")
    is_active = models.BooleanField(default=True, verbose_name="Activa")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Descripción")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio original")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Categoría")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")
    is_featured = models.BooleanField(default=False, verbose_name="Destacado")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="Peso (kg)")
    dimensions = models.CharField(max_length=100, blank=True, verbose_name="Dimensiones")
    sku = models.CharField(max_length=50, unique=True, verbose_name="SKU")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})

    def get_discount_percentage(self):
        # Solo mostrar descuento si el producto es destacado y tiene precio original
        if self.is_featured and self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0

    def has_discount(self):
        """Verificar si el producto tiene descuento (solo productos destacados)"""
        return self.is_featured and self.original_price and self.original_price > self.price

    @property
    def main_image(self):
        return self.images.filter(is_main=True).first() or self.images.first()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Producto")
    image = models.ImageField(upload_to='products/', verbose_name="Imagen", null=True, blank=True)
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Texto alternativo")
    is_main = models.BooleanField(default=False, verbose_name="Imagen principal")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Imagen de producto"
        verbose_name_plural = "Imágenes de productos"
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"Imagen de {self.product.name}"

    def save(self, *args, **kwargs):
        if self.is_main:
            # Desactivar otras imágenes principales del mismo producto
            ProductImage.objects.filter(product=self.product, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)

    def get_image_url(self):
        """Obtener URL de la imagen"""
        if self.image:
            return self.image.url
        return None

    def get_image_data_base64(self):
        """Obtener los datos de imagen en formato base64 para usar en templates"""
        if self.image:
            import base64
            with open(self.image.path, 'rb') as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        return None


class ProductVariant(models.Model):
    """Variantes de productos (color, tamaño, material, etc.)"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', verbose_name="Producto")
    name = models.CharField(max_length=100, verbose_name="Nombre de la variante")
    value = models.CharField(max_length=100, verbose_name="Valor de la variante")
    sku = models.CharField(max_length=50, unique=True, verbose_name="SKU de variante")
    price_modifier = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Modificador de precio")
    is_active = models.BooleanField(default=True, verbose_name="Activa")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Variante de producto"
        verbose_name_plural = "Variantes de productos"
        unique_together = ['product', 'name', 'value']
        ordering = ['name', 'value']

    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"

    def get_final_price(self):
        """Obtener precio final de la variante"""
        return self.product.price + self.price_modifier

    def save(self, *args, **kwargs):
        if not self.sku:
            # Generar SKU único para la variante
            base_sku = f"{self.product.sku}-{self.name[:3].upper()}-{self.value[:3].upper()}"
            counter = 1
            while ProductVariant.objects.filter(sku=base_sku).exists():
                base_sku = f"{self.product.sku}-{self.name[:3].upper()}-{self.value[:3].upper()}-{counter}"
                counter += 1
            self.sku = base_sku
        super().save(*args, **kwargs)


class ItemStock(models.Model):
    """Stock separado para productos y variantes"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_items', verbose_name="Producto")
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True, related_name='stock_items', verbose_name="Variante")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Cantidad disponible")
    reserved_quantity = models.PositiveIntegerField(default=0, verbose_name="Cantidad reservada")
    min_stock_level = models.PositiveIntegerField(default=5, verbose_name="Nivel mínimo de stock")
    location = models.CharField(max_length=100, blank=True, verbose_name="Ubicación en almacén")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Stock de item"
        verbose_name_plural = "Stock de items"
        unique_together = ['product', 'variant']
        ordering = ['product__name', 'variant__name']

    def __str__(self):
        if self.variant:
            return f"{self.product.name} - {self.variant.name}: {self.variant.value} (Stock: {self.quantity})"
        return f"{self.product.name} (Stock: {self.quantity})"

    @property
    def available_quantity(self):
        """Cantidad realmente disponible (total - reservada)"""
        return self.quantity - self.reserved_quantity

    @property
    def is_low_stock(self):
        """Verificar si el stock está bajo"""
        return self.available_quantity <= self.min_stock_level

    def reserve_stock(self, quantity):
        """Reservar stock para el carrito"""
        if self.available_quantity >= quantity:
            self.reserved_quantity += quantity
            self.save()
            return True
        return False

    def release_stock(self, quantity):
        """Liberar stock reservado"""
        if self.reserved_quantity >= quantity:
            self.reserved_quantity -= quantity
            self.save()
            return True
        return False

    def consume_stock(self, quantity):
        """Consumir stock (para órdenes confirmadas)"""
        if self.available_quantity >= quantity:
            self.quantity -= quantity
            self.save()
            return True
        return False

    def add_stock(self, quantity):
        """Agregar stock"""
        self.quantity += quantity
        self.save()

    def save(self, *args, **kwargs):
        # Si no hay variante, crear un stock item por defecto para el producto
        if not self.variant:
            # Verificar si ya existe un stock item para este producto sin variante
            existing = ItemStock.objects.filter(product=self.product, variant__isnull=True).exclude(id=self.id)
            if existing.exists():
                return  # No crear duplicados
        super().save(*args, **kwargs)
