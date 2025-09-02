from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, ProductVariant, ItemStock


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image_data', 'image_type', 'filename', 'alt_text', 'is_main', 'order']


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ['name', 'value', 'sku', 'price_modifier', 'is_active']


class ItemStockInline(admin.TabularInline):
    model = ItemStock
    extra = 1
    fields = ['variant', 'quantity', 'reserved_quantity', 'min_stock_level', 'location']
    readonly_fields = ['reserved_quantity']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'created_at']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock_display', 'is_active', 'is_featured', 'created_at']
    list_filter = ['is_active', 'is_featured', 'category', 'created_at']
    search_fields = ['name', 'description', 'sku']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    inlines = [ProductImageInline, ProductVariantInline, ItemStockInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'slug', 'description', 'category', 'sku')
        }),
        ('Precios', {
            'fields': ('price', 'original_price')
        }),
        ('Stock y Estado', {
            'fields': ('stock', 'is_active', 'is_featured')
        }),
        ('Características', {
            'fields': ('weight', 'dimensions'),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def stock_display(self, obj):
        """Mostrar stock total incluyendo variantes"""
        total_stock = obj.stock
        variants_stock = sum(item.quantity for item in obj.stock_items.all())
        return f"{total_stock} + {variants_stock} (variantes)"
    stock_display.short_description = 'Stock Total'


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'value', 'sku', 'price_modifier', 'final_price', 'is_active']
    list_filter = ['is_active', 'name', 'product__category']
    search_fields = ['product__name', 'name', 'value', 'sku']
    ordering = ['product__name', 'name', 'value']
    readonly_fields = ['sku', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Información de la Variante', {
            'fields': ('product', 'name', 'value', 'sku')
        }),
        ('Precio', {
            'fields': ('price_modifier',)
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def final_price(self, obj):
        """Mostrar precio final de la variante"""
        return f"RD$ {obj.get_final_price():.2f}"
    final_price.short_description = 'Precio Final'


@admin.register(ItemStock)
class ItemStockAdmin(admin.ModelAdmin):
    list_display = ['product', 'variant_display', 'quantity', 'reserved_quantity', 'available_quantity', 'is_low_stock', 'location']
    list_filter = ['product__category', 'variant__name']
    search_fields = ['product__name', 'variant__name', 'variant__value', 'location']
    ordering = ['product__name', 'variant__name']
    readonly_fields = ['available_quantity', 'is_low_stock', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Producto y Variante', {
            'fields': ('product', 'variant')
        }),
        ('Stock', {
            'fields': ('quantity', 'reserved_quantity', 'available_quantity', 'min_stock_level')
        }),
        ('Estado', {
            'fields': ('is_low_stock',)
        }),
        ('Ubicación', {
            'fields': ('location',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def variant_display(self, obj):
        """Mostrar información de la variante"""
        if obj.variant:
            return f"{obj.variant.name}: {obj.variant.value}"
        return "Sin variante"
    variant_display.short_description = 'Variante'
    
    def available_quantity(self, obj):
        """Mostrar cantidad disponible con color"""
        if obj.is_low_stock:
            return format_html('<span style="color: red;">{}</span>', obj.available_quantity)
        return obj.available_quantity
    available_quantity.short_description = 'Disponible'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'filename', 'is_main', 'order', 'created_at']
    list_filter = ['is_main', 'product__category']
    search_fields = ['product__name', 'filename', 'alt_text']
    ordering = ['product__name', 'order']
    readonly_fields = ['created_at']
