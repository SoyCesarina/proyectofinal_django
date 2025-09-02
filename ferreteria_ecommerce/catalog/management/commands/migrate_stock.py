from django.core.management.base import BaseCommand
from django.db import transaction
from catalog.models import Product, ItemStock


class Command(BaseCommand):
    help = 'Migra el stock existente de productos al nuevo sistema ItemStock'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Ejecutar sin hacer cambios reales en la base de datos',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('MODO DRY-RUN: No se harán cambios reales en la base de datos')
            )
        
        self.stdout.write('Iniciando migración de stock...')
        
        products = Product.objects.all()
        total_products = products.count()
        migrated_count = 0
        errors = []
        
        for product in products:
            try:
                if dry_run:
                    self.stdout.write(f'[DRY-RUN] Procesando: {product.name} (Stock actual: {product.stock})')
                else:
                    with transaction.atomic():
                        # Crear ItemStock para el producto principal
                        stock_item, created = ItemStock.objects.get_or_create(
                            product=product,
                            variant=None,
                            defaults={
                                'quantity': product.stock,
                                'reserved_quantity': 0,
                                'min_stock_level': 5,
                                'location': 'Almacén Principal'
                            }
                        )
                        
                        if not created:
                            # Actualizar stock existente
                            stock_item.quantity = product.stock
                            stock_item.save()
                        
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ {product.name}: Stock migrado a {stock_item.quantity}')
                        )
                        migrated_count += 1
                        
            except Exception as e:
                error_msg = f'Error procesando {product.name}: {str(e)}'
                self.stdout.write(self.style.ERROR(error_msg))
                errors.append(error_msg)
        
        # Resumen
        self.stdout.write('\n' + '='*50)
        self.stdout.write('RESUMEN DE MIGRACIÓN')
        self.stdout.write('='*50)
        self.stdout.write(f'Total de productos: {total_products}')
        self.stdout.write(f'Migrados exitosamente: {migrated_count}')
        self.stdout.write(f'Errores: {len(errors)}')
        
        if errors:
            self.stdout.write('\nErrores encontrados:')
            for error in errors:
                self.stdout.write(self.style.ERROR(f'  - {error}'))
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('\nPara ejecutar la migración real, ejecuta sin --dry-run')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('\n¡Migración completada exitosamente!')
            )
