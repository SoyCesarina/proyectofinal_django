from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from promotions.models import Coupon


class Command(BaseCommand):
    help = 'Corregir las fechas de los cupones para que funcionen correctamente'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Corregir todos los cupones existentes',
        )

    def handle(self, *args, **options):
        # Fecha actual con zona horaria
        now = timezone.now()
        
        if options['all']:
            # Corregir todos los cupones existentes
            coupons = Coupon.objects.all()
        else:
            # Solo corregir cupones específicos para productos destacados
            coupons = Coupon.objects.filter(
                code__in=['DESTACADOS13', 'DESTACADOS9', 'FEATURED13', 'FEATURED9', 
                         'BIENVENIDA10', 'DESCUENTO50', 'SUPER20', 'FERRETERIA25', 
                         'AHORRO100', 'PRIMERA15', 'ESPECIAL75', 'MEGA30']
            )
        
        fixed_count = 0
        
        for coupon in coupons:
            # Verificar si las fechas necesitan corrección
            needs_fix = False
            
            # Si las fechas son naive (sin zona horaria), convertirlas
            if timezone.is_naive(coupon.valid_from):
                coupon.valid_from = timezone.make_aware(coupon.valid_from)
                needs_fix = True
                
            if timezone.is_naive(coupon.valid_to):
                coupon.valid_to = timezone.make_aware(coupon.valid_to)
                needs_fix = True
            
            # Si las fechas están en el pasado, actualizarlas
            if coupon.valid_from > now:
                # Si la fecha de inicio está en el futuro, ponerla ahora
                coupon.valid_from = now
                needs_fix = True
                
            if coupon.valid_to <= now:
                # Si la fecha de fin está en el pasado, extenderla
                coupon.valid_to = now + timezone.timedelta(days=365)
                needs_fix = True
            
            # Asegurar que el cupón esté activo
            if not coupon.is_active:
                coupon.is_active = True
                needs_fix = True
            
            if needs_fix:
                coupon.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Cupón corregido: {coupon.code}')
                )
                fixed_count += 1
            else:
                self.stdout.write(
                    self.style.WARNING(f'Cupón ya está correcto: {coupon.code}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nResumen:')
        )
        self.stdout.write(
            f'   - Cupones corregidos: {fixed_count}'
        )
        
        # Verificar el estado final de los cupones
        self.stdout.write(
            self.style.SUCCESS(f'\nEstado final de los cupones:')
        )
        for coupon in Coupon.objects.filter(is_active=True).order_by('code'):
            is_valid = coupon.is_valid()
            status = "Válido" if is_valid else "Inválido"
            self.stdout.write(
                f'   - {coupon.code}: {status} (Desde: {coupon.valid_from.strftime("%Y-%m-%d %H:%M")}, Hasta: {coupon.valid_to.strftime("%Y-%m-%d %H:%M")})'
            )
        
        # Crear cupones de ejemplo si no existen
        self.stdout.write(
            self.style.SUCCESS(f'\nCreando cupones de ejemplo...')
        )
        
        example_coupons = [
            {
                'code': 'TEST10',
                'description': 'Cupón de prueba - 10% de descuento',
                'discount_type': 'percentage',
                'discount_value': Decimal('10.00'),
                'min_amount': Decimal('100.00'),
                'max_discount': Decimal('200.00'),
                'valid_from': now,
                'valid_to': now + timezone.timedelta(days=365),
                'usage_limit': 1000,
            },
            {
                'code': 'PRUEBA20',
                'description': 'Cupón de prueba - 20% de descuento',
                'discount_type': 'percentage',
                'discount_value': Decimal('20.00'),
                'min_amount': Decimal('200.00'),
                'max_discount': Decimal('400.00'),
                'valid_from': now,
                'valid_to': now + timezone.timedelta(days=365),
                'usage_limit': 500,
            }
        ]
        
        for coupon_data in example_coupons:
            coupon, created = Coupon.objects.get_or_create(
                code=coupon_data['code'],
                defaults=coupon_data
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Cupón de prueba creado: {coupon.code}')
                )
            else:
                # Actualizar cupón existente
                for key, value in coupon_data.items():
                    setattr(coupon, key, value)
                coupon.save()
                self.stdout.write(
                    self.style.WARNING(f'Cupón de prueba actualizado: {coupon.code}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n¡Cupones corregidos exitosamente!')
        )
        self.stdout.write(
            f'   - Puedes probar con: TEST10, PRUEBA20, DESTACADOS13, DESTACADOS9'
        )
