from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import transaction
from django.contrib.sessions.models import Session
from .models import Order, OrderItem
from .forms import CheckoutForm
from cart.views import get_or_create_cart
from promotions.models import Coupon
from catalog.models import ItemStock


def checkout(request):
    """Vista del checkout"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    if not cart_items:
        messages.error(request, 'Tu carrito está vacío.')
        return redirect('cart:cart_detail')
    
    # Obtener cupón aplicado si existe
    applied_coupon = None
    discount_amount = 0
    
    if 'applied_coupon_id' in request.session:
        try:
            applied_coupon = Coupon.objects.get(id=request.session['applied_coupon_id'])
            if applied_coupon.is_valid():
                cart_total = cart.get_total()
                if cart_total >= applied_coupon.min_amount:
                    discount_amount = applied_coupon.calculate_discount(cart_total)
        except Coupon.DoesNotExist:
            # Si el cupón no existe, limpiarlo de la sesión
            if 'applied_coupon_id' in request.session:
                del request.session['applied_coupon_id']
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Crear la orden
                    order = form.save(commit=False)
                    # Corregir el manejo de sesiones
                    order.session = Session.objects.get(session_key=request.session.session_key)
                    order.subtotal = cart.get_total()
                    order.discount = discount_amount
                    order.total = order.subtotal - order.discount
                    if applied_coupon:
                        order.coupon = applied_coupon
                    order.save()
                    
                    # Crear items de la orden con variantes
                    for cart_item in cart_items:
                        OrderItem.objects.create(
                            order=order,
                            product=cart_item.product,
                            variant=cart_item.variant,  # Agregar variante
                            quantity=cart_item.quantity,
                            price=cart_item.price,
                            total=cart_item.get_total()
                        )
                        
                        # Consumir stock reservado y liberar la reserva
                        if cart_item.variant:
                            try:
                                stock_item = ItemStock.objects.get(product=cart_item.product, variant=cart_item.variant)
                                stock_item.consume_stock(cart_item.quantity)
                                stock_item.release_stock(cart_item.quantity)
                            except ItemStock.DoesNotExist:
                                pass
                        else:
                            try:
                                stock_item = ItemStock.objects.get(product=cart_item.product, variant__isnull=True)
                                stock_item.consume_stock(cart_item.quantity)
                                stock_item.release_stock(cart_item.quantity)
                            except ItemStock.DoesNotExist:
                                pass
                    
                    # Limpiar carrito y cupón aplicado
                    cart.clear()
                    if 'applied_coupon_id' in request.session:
                        del request.session['applied_coupon_id']
                    
                    messages.success(request, f'Orden {order.order_number} creada exitosamente.')
                    return redirect('orders:order_detail', order_number=order.order_number)
                    
            except Exception as e:
                messages.error(request, 'Error al procesar la orden. Inténtalo de nuevo.')
    else:
        form = CheckoutForm()
    
    # Calcular el total final con descuento
    cart_total = cart.get_total()
    final_total = cart_total - discount_amount
    
    context = {
        'form': form,
        'cart': cart,
        'cart_items': cart_items,
        'applied_coupon': applied_coupon,
        'discount_amount': discount_amount,
        'final_total': final_total,
    }
    return render(request, 'orders/checkout.html', context)


def order_detail(request, order_number):
    """Detalle de una orden"""
    order = get_object_or_404(Order, order_number=order_number)
    
    # Verificar que la orden pertenece a la sesión actual
    if order.session.session_key != request.session.session_key:
        messages.error(request, 'No tienes permisos para ver esta orden.')
        return redirect('catalog:home')
    
    context = {
        'order': order,
    }
    return render(request, 'orders/order_detail.html', context)


@require_POST
def apply_coupon(request):
    """Aplicar cupón de descuento"""
    coupon_code = request.POST.get('coupon_code', '').strip()
    
    if not coupon_code:
        messages.error(request, 'Por favor ingresa un código de cupón.')
        return redirect('cart:cart_detail')
    
    try:
        coupon = Coupon.objects.get(code=coupon_code)
        if not coupon.is_valid():
            messages.error(request, 'Este cupón no es válido o ha expirado.')
            return redirect('cart:cart_detail')
        
        cart = get_or_create_cart(request)
        cart_total = cart.get_total()
        
        if cart_total < coupon.min_amount:
            messages.error(request, f'El monto mínimo para usar este cupón es ${coupon.min_amount}.')
            return redirect('cart:cart_detail')
        
        # Guardar el cupón en la sesión para usarlo en el checkout
        request.session['applied_coupon_id'] = coupon.id
        discount = coupon.calculate_discount(cart_total)
        
        messages.success(request, f'Cupón aplicado. Descuento: ${discount}')
        
    except Coupon.DoesNotExist:
        messages.error(request, 'Código de cupón inválido.')
    
    return redirect('cart:cart_detail')


def remove_coupon(request):
    """Remover cupón aplicado"""
    if 'applied_coupon_id' in request.session:
        del request.session['applied_coupon_id']
        messages.success(request, 'Cupón removido.')
    
    return redirect('cart:cart_detail')
