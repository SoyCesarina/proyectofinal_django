from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.utils import timezone
from catalog.models import Category, Product, ProductVariant, ItemStock
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem
from promotions.models import Coupon
from warehouse.models import InventoryMovement, Shipment


class Command(BaseCommand):
    help = 'Prueba el flujo completo del e-commerce'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando prueba del flujo de e-commerce...'))
        
        try:
            # 1. Crear categoría de prueba
            category, created = Category.objects.get_or_create(
                name='Herramientas Manuales',
                slug='herramientas-manuales',
                defaults={'description': 'Herramientas manuales de calidad'}
            )
            if created:
                self.stdout.write(f'✓ Categoría creada: {category.name}')
            else:
                self.stdout.write(f'✓ Categoría existente: {category.name}')
            
            # 2. Crear producto de prueba
            product, created = Product.objects.get_or_create(
                name='Martillo Profesional',
                slug='martillo-profesional',
                defaults={
                    'description': 'Martillo profesional de alta calidad',
                    'price': 25.99,
                    'category': category,
                    'stock': 100,
                    'is_featured': True,
                    'sku': 'MART-001'
                }
            )
            if created:
                self.stdout.write(f'✓ Producto creado: {product.name}')
            else:
                self.stdout.write(f'✓ Producto existente: {product.name}')
            
            # 3. Crear variante del producto
            variant, created = ProductVariant.objects.get_or_create(
                product=product,
                name='Peso',
                value='500g',
                defaults={
                    'sku': 'MART-001-500G',
                    'price_modifier': 0
                }
            )
            if created:
                self.stdout.write(f'✓ Variante creada: {variant.name}: {variant.value}')
            else:
                self.stdout.write(f'✓ Variante existente: {variant.name}: {variant.value}')
            
            # 4. Crear stock para el producto y variante
            stock_product, created = ItemStock.objects.get_or_create(
                product=product,
                variant=None,
                defaults={'quantity': 50, 'reserved_quantity': 0}
            )
            if created:
                self.stdout.write(f'✓ Stock creado para producto: {stock_product.quantity} unidades')
            else:
                self.stdout.write(f'✓ Stock existente para producto: {stock_product.quantity} unidades')
            
            stock_variant, created = ItemStock.objects.get_or_create(
                product=product,
                variant=variant,
                defaults={'quantity': 50, 'reserved_quantity': 0}
            )
            if created:
                self.stdout.write(f'✓ Stock creado para variante: {stock_variant.quantity} unidades')
            else:
                self.stdout.write(f'✓ Stock existente para variante: {stock_variant.quantity} unidades')
            
            # 5. Crear cupón de prueba
            coupon, created = Coupon.objects.get_or_create(
                code='PRUEBA20',
                defaults={
                    'description': 'Cupón de prueba 20%',
                    'discount_type': 'percentage',
                    'discount_value': 20,
                    'min_amount': 10.00,
                    'valid_from': timezone.now(),
                    'valid_to': timezone.now() + timezone.timedelta(days=30),
                    'usage_limit': 100
                }
            )
            if created:
                self.stdout.write(f'✓ Cupón creado: {coupon.code}')
            else:
                self.stdout.write(f'✓ Cupón existente: {coupon.code}')
            
            # 6. Crear sesión de prueba
            session = Session.objects.create(
                session_key='test_session_123',
                expire_date=timezone.now() + timezone.timedelta(days=1)
            )
            self.stdout.write(f'✓ Sesión de prueba creada: {session.session_key}')
            
            # 7. Crear carrito de prueba
            cart, created = Cart.objects.get_or_create(session=session)
            if created:
                self.stdout.write(f'✓ Carrito creado para sesión: {cart.id}')
            else:
                self.stdout.write(f'✓ Carrito existente para sesión: {cart.id}')
            
            # 8. Agregar productos al carrito
            cart_item_product, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                variant=None,
                defaults={'quantity': 2, 'price': product.price}
            )
            if created:
                self.stdout.write(f'✓ Producto agregado al carrito: {cart_item_product.quantity}x {product.name}')
            else:
                self.stdout.write(f'✓ Producto existente en carrito: {cart_item_product.quantity}x {product.name}')
            
            cart_item_variant, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                variant=variant,
                defaults={'quantity': 1, 'price': variant.get_final_price()}
            )
            if created:
                self.stdout.write(f'✓ Variante agregada al carrito: {cart_item_variant.quantity}x {variant.name}: {variant.value}')
            else:
                self.stdout.write(f'✓ Variante existente en carrito: {cart_item_variant.quantity}x {variant.name}: {variant.value}')
            
            # 9. Verificar total del carrito
            cart_total = cart.get_total()
            self.stdout.write(f'✓ Total del carrito: RD$ {cart_total:.2f}')
            
            # 10. Crear orden de prueba
            order, created = Order.objects.get_or_create(
                order_number='TEST-ORDER-001',
                defaults={
                    'session': session,
                    'customer_name': 'Cliente de Prueba',
                    'customer_email': 'test@example.com',
                    'customer_phone': '809-123-4567',
                    'shipping_address': 'Calle de Prueba #123',
                    'shipping_city': 'Santo Domingo',
                    'shipping_state': 'Distrito Nacional',
                    'shipping_zip_code': '10101',
                    'status': 'confirmed',
                    'subtotal': cart_total,
                    'discount': 0,
                    'total': cart_total
                }
            )
            if created:
                self.stdout.write(f'✓ Orden creada: {order.order_number}')
            else:
                self.stdout.write(f'✓ Orden existente: {order.order_number}')
            
            # 11. Crear items de la orden
            for cart_item in cart.items.all():
                order_item, created = OrderItem.objects.get_or_create(
                    order=order,
                    product=cart_item.product,
                    variant=cart_item.variant,
                    defaults={
                        'quantity': cart_item.quantity,
                        'price': cart_item.price,
                        'total': cart_item.get_total()
                    }
                )
                if created:
                    self.stdout.write(f'✓ Item de orden creado: {order_item.quantity}x {order_item.get_product_display_name()}')
                else:
                    self.stdout.write(f'✓ Item de orden existente: {order_item.quantity}x {order_item.get_product_display_name()}')
            
            # 12. Verificar que se pueden crear movimientos de inventario
            movement, created = InventoryMovement.objects.get_or_create(
                product=product,
                variant=variant,
                movement_type='out',
                quantity=1,
                reason='Prueba del sistema',
                order=order
            )
            if created:
                self.stdout.write(f'✓ Movimiento de inventario creado: {movement.get_movement_type_display()}')
            else:
                self.stdout.write(f'✓ Movimiento de inventario existente: {movement.get_movement_type_display()}')
            
            # 13. Verificar que se puede crear un despacho
            shipment, created = Shipment.objects.get_or_create(
                order=order,
                defaults={
                    'tracking_number': 'TRACK-123',
                    'carrier': 'Servicio de Prueba',
                    'notes': 'Despacho de prueba'
                }
            )
            if created:
                self.stdout.write(f'✓ Despacho creado para orden: {shipment.order.order_number}')
            else:
                self.stdout.write(f'✓ Despacho existente para orden: {shipment.order.order_number}')
            
            self.stdout.write(self.style.SUCCESS('\n🎉 ¡Prueba del flujo de e-commerce completada exitosamente!'))
            self.stdout.write('\nResumen de la prueba:')
            self.stdout.write(f'• Categoría: {category.name}')
            self.stdout.write(f'• Producto: {product.name}')
            self.stdout.write(f'• Variante: {variant.name}: {variant.value}')
            self.stdout.write(f'• Cupón: {coupon.code}')
            self.stdout.write(f'• Carrito: {cart.get_item_count()} items, Total: RD$ {cart_total:.2f}')
            self.stdout.write(f'• Orden: {order.order_number}, Estado: {order.get_status_display()}')
            self.stdout.write(f'• Despacho: {shipment.id}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error durante la prueba: {str(e)}'))
            raise
