from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils.text import slugify
from catalog.models import Category, Product, ProductImage, ProductVariant, ItemStock
from decimal import Decimal
import os


class Command(BaseCommand):
    help = 'Poblar la base de datos con categorías y productos de ejemplo'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando población de la base de datos...')
        
        # Crear categorías principales
        categories_data = [
            {
                'name': 'Herramientas Manuales',
                'description': 'Herramientas básicas para trabajos manuales',
                'children': [
                    {'name': 'Martillos', 'description': 'Diferentes tipos de martillos'},
                    {'name': 'Destornilladores', 'description': 'Destornilladores de varias medidas'},
                    {'name': 'Alicates', 'description': 'Alicates para diferentes usos'},
                ]
            },
            {
                'name': 'Herramientas Eléctricas',
                'description': 'Herramientas eléctricas profesionales',
                'children': [
                    {'name': 'Taladros', 'description': 'Taladros eléctricos y de batería'},
                    {'name': 'Sierras', 'description': 'Sierras eléctricas y circulares'},
                    {'name': 'Lijadoras', 'description': 'Lijadoras orbitales y de banda'},
                ]
            },
            {
                'name': 'Materiales de Construcción',
                'description': 'Materiales básicos para construcción',
                'children': [
                    {'name': 'Cemento', 'description': 'Cemento Portland y especiales'},
                    {'name': 'Arena', 'description': 'Arena fina y gruesa'},
                    {'name': 'Grava', 'description': 'Grava de diferentes tamaños'},
                ]
            },
            {
                'name': 'Plomería',
                'description': 'Productos para instalaciones de plomería',
                'children': [
                    {'name': 'Tuberías', 'description': 'Tuberías PVC y metálicas'},
                    {'name': 'Válvulas', 'description': 'Válvulas de diferentes tipos'},
                    {'name': 'Accesorios', 'description': 'Codos, tees y otros accesorios'},
                ]
            },
            {
                'name': 'Electricidad',
                'description': 'Materiales para instalaciones eléctricas',
                'children': [
                    {'name': 'Cables', 'description': 'Cables eléctricos de diferentes calibres'},
                    {'name': 'Interruptores', 'description': 'Interruptores y tomacorrientes'},
                    {'name': 'Iluminación', 'description': 'Lámparas y accesorios de iluminación'},
                ]
            }
        ]
        
        # Crear categorías
        created_categories = {}
        for cat_data in categories_data:
            parent_category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'slug': slugify(cat_data['name']),
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Categoría creada: {parent_category.name}')
            created_categories[parent_category.name] = parent_category
            
            # Crear subcategorías
            for child_data in cat_data['children']:
                child_category, created = Category.objects.get_or_create(
                    name=child_data['name'],
                    parent=parent_category,
                    defaults={
                        'description': child_data['description'],
                        'slug': slugify(child_data['name']),
                        'is_active': True
                    }
                )
                if created:
                    self.stdout.write(f'  Subcategoría creada: {child_category.name}')
                created_categories[child_category.name] = child_category
        
        # Crear productos de ejemplo
        products_data = [
            {
                'name': 'Martillo de Carpintero 16oz',
                'description': 'Martillo profesional de carpintero con mango de madera dura y cabeza de acero forjado. Ideal para trabajos de construcción y carpintería.',
                'category': 'Martillos',
                'price': Decimal('850.00'),
                'original_price': Decimal('1200.00'),
                'stock': 25,
                'is_featured': True,
                'sku': 'MART-16OZ-001',
                'weight': Decimal('0.45'),
                'dimensions': '30 x 15 x 8 cm'
            },
            {
                'name': 'Destornillador Phillips #2',
                'description': 'Destornillador Phillips de alta calidad con mango ergonómico y punta magnetizada. Incluye 3 puntas intercambiables.',
                'category': 'Destornilladores',
                'price': Decimal('450.00'),
                'original_price': None,
                'stock': 50,
                'is_featured': False,
                'sku': 'DEST-PH2-001',
                'weight': Decimal('0.15'),
                'dimensions': '25 x 3 x 3 cm'
            },
            {
                'name': 'Taladro Eléctrico 1/2"',
                'description': 'Taladro eléctrico profesional de 1/2 pulgada con velocidad variable y reversa. Incluye maletín y accesorios.',
                'category': 'Taladros',
                'price': Decimal('3500.00'),
                'original_price': Decimal('4200.00'),
                'stock': 15,
                'is_featured': True,
                'sku': 'TAL-ELEC-001',
                'weight': Decimal('2.5'),
                'dimensions': '35 x 20 x 15 cm'
            },
            {
                'name': 'Cemento Portland Tipo I',
                'description': 'Cemento Portland Tipo I de alta resistencia, ideal para construcciones generales. Saco de 42.5 kg.',
                'category': 'Cemento',
                'price': Decimal('450.00'),
                'original_price': None,
                'stock': 100,
                'is_featured': False,
                'sku': 'CEM-PORT-001',
                'weight': Decimal('42.5'),
                'dimensions': '60 x 40 x 15 cm'
            },
            {
                'name': 'Tubería PVC 4" x 3m',
                'description': 'Tubería PVC de 4 pulgadas de diámetro y 3 metros de longitud. Ideal para drenajes y sistemas de alcantarillado.',
                'category': 'Tuberías',
                'price': Decimal('1200.00'),
                'original_price': Decimal('1500.00'),
                'stock': 30,
                'is_featured': True,
                'sku': 'TUB-PVC-4-001',
                'weight': Decimal('8.5'),
                'dimensions': '300 x 10 x 10 cm'
            },
            {
                'name': 'Cable Eléctrico #12 AWG',
                'description': 'Cable eléctrico THHN #12 AWG de 100 metros. Ideal para instalaciones residenciales y comerciales.',
                'category': 'Cables',
                'price': Decimal('2800.00'),
                'original_price': None,
                'stock': 20,
                'is_featured': False,
                'sku': 'CAB-ELEC-12-001',
                'weight': Decimal('12.0'),
                'dimensions': '100 x 0.5 x 0.5 cm'
            }
        ]
        
        # Crear productos
        for prod_data in products_data:
            category = created_categories[prod_data['category']]
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'description': prod_data['description'],
                    'slug': slugify(prod_data['name']),
                    'category': category,
                    'price': prod_data['price'],
                    'original_price': prod_data['original_price'],
                    'stock': prod_data['stock'],
                    'is_featured': prod_data['is_featured'],
                    'sku': prod_data['sku'],
                    'weight': prod_data['weight'],
                    'dimensions': prod_data['dimensions'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f'Producto creado: {product.name}')
                
                # Crear stock para el producto
                ItemStock.objects.create(
                    product=product,
                    quantity=prod_data['stock'],
                    min_stock_level=5,
                    location='Estante Principal'
                )
                
                # Crear imagen de producto (placeholder)
                ProductImage.objects.create(
                    product=product,
                    alt_text=product.name,
                    is_main=True,
                    order=1
                )
                
                # Crear variantes si es necesario
                if 'Martillo' in product.name:
                    ProductVariant.objects.create(
                        product=product,
                        name='Color',
                        value='Negro',
                        price_modifier=Decimal('0.00')
                    )
                    ProductVariant.objects.create(
                        product=product,
                        name='Color',
                        value='Rojo',
                        price_modifier=Decimal('50.00')
                    )
                elif 'Taladro' in product.name:
                    ProductVariant.objects.create(
                        product=product,
                        name='Color',
                        value='Azul',
                        price_modifier=Decimal('0.00')
                    )
                    ProductVariant.objects.create(
                        product=product,
                        name='Color',
                        value='Negro',
                        price_modifier=Decimal('100.00')
                    )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Base de datos poblada exitosamente con {len(created_categories)} categorías y {len(products_data)} productos'
            )
        )
