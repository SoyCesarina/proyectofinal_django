from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from promotions.models import Coupon


class Command(BaseCommand):
    help = 'Crear cupones de ejemplo en la base de datos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpiar cupones existentes antes de crear nuevos',
        )

    def handle(self, *args, **options):
        if options['clear']:
            Coupon.objects.all().delete()
            self.stdout.write(
                self.style.WARNING('Cupones existentes eliminados.')
            )

        # Fecha actual con zona horaria
        now = timezone.now()
        
        # Importar datetime para crear fechas con zona horaria
        from datetime import datetime, timedelta
        
        # Cupones de ejemplo
        coupons_data = [
            {
                'code': 'BIENVENIDA10',
                'description': 'Cupón de bienvenida - 10% de descuento',
                'discount_type': 'percentage',
                'discount_value': Decimal('10.00'),
                'min_amount': Decimal('1000.00'),
                'max_discount': Decimal('500.00'),
                'valid_from': now,
                'valid_to': now + timezone.timedelta(days=365),
                'usage_limit': 1000,
            },
            {
                'code': 'DESCUENTO50',
                'description': 'Descuento fijo de RD$ 50',
                'discount_type': 'fixed',
                'discount_value': Decimal('50.00'),
                'min_amount': Decimal('500.00'),
                'max_discount': None,
                'valid_from': now,
                'valid_to': now + timezone.timedelta(days=180),
                'usage_limit': 500,
            },
            {
                'code': 'SUPER20',
                'description': 'Super descuento - 20% de descuento',
                'discount_type': 'percentage',
                'discount_value': Decimal('20.00'),
                'min_amount': Decimal('2000.00'),
                'max_discount': Decimal('1000.00'),
                'valid_from': now,
                'valid_to': now + timezone.timedelta(days=90),
                'usage_limit': 200,
            },
            {
                'code': 'FERRETERIA25',
                'description': 'Cupón especial ferretería - 25% de descuento',
                'discount_type': 'percentage',
                'discount_value': Decimal('25.00'),
                'min_amount': Decimal('1500.00'),
                'max_discount': Decimal('750.00'),
                'valid_from': now,
                'valid_to': now + timezone.timedelta(days=120),
                'usage_limit': 300,
            },
            {
                'code': 'AHORRO100',
                'description': 'Ahorro de RD$ 100 en compras grandes',
                'discount_type': 'fixed',
                'discount_value': Decimal('100.00'),
                'min_amount': Decimal('1000.00'),
                'max_discount': None,
                'valid_from': now,
                'valid_to': now + timezone.timedelta(days=60),
                'usage_limit': 150,
            },
            {
                'code': 'PRIMERA15',
                'description': 'Primera compra - 15% de descuento',
                'discount_type': 'percentage',
                'discount_value': Decimal('15.00'),
                'min_amount': Decimal('800.00'),
                'max_discount': Decimal('400.00'),
                'valid_from': now,
                'valid_to': now + timezone.timedelta(days=200),
                'usage_limit': 400,
            },
            {
                'code': 'ESPECIAL75',
                'description': 'Descuento especial de RD$ 75',
                'discount_type': 'fixed',
                'discount_value': Decimal('75.00'),
                'min_amount': Decimal('750.00'),
                'max_discount': None,
                'valid_from': now,
                'valid_to': now + timezone.timedelta(days=150),
                'usage_limit': 250,
            },
            {
                'code': 'MEGA30',
                'description': 'Mega descuento - 30% de descuento',
                'discount_type': 'percentage',
                'discount_value': Decimal('30.00'),
                'min_amount': Decimal('3000.00'),
                'max_discount': Decimal('1500.00'),
                'valid_from': now,
                'valid_to': now + timezone.timedelta(days=45),
                'usage_limit': 100,
            }
        ]
        
        created_count = 0
        updated_count = 0
        
        for coupon_data in coupons_data:
            coupon, created = Coupon.objects.get_or_create(
                code=coupon_data['code'],
                defaults=coupon_data
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Cupón creado: {coupon.code}')
                )
                created_count += 1
            else:
                # Actualizar cupón existente
                for key, value in coupon_data.items():
                    setattr(coupon, key, value)
                coupon.save()
                self.stdout.write(
                    self.style.WARNING(f'Cupón actualizado: {coupon.code}')
                )
                updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'\nResumen:')
        )
        self.stdout.write(
            f'   - Cupones creados: {created_count}'
        )
        self.stdout.write(
            f'   - Cupones actualizados: {updated_count}'
        )
        self.stdout.write(
            f'   - Total de cupones: {Coupon.objects.count()}'
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nCupones disponibles:')
        )
        for coupon in Coupon.objects.filter(is_active=True).order_by('code'):
            discount_info = f"{coupon.discount_value}%"
            if coupon.discount_type == 'fixed':
                discount_info = f"RD$ {coupon.discount_value}"
            
            self.stdout.write(
                f'   - {coupon.code}: {discount_info} (mín: RD$ {coupon.min_amount})'
            )
