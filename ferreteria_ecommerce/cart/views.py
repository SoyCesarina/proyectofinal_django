from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.sessions.models import Session
from catalog.models import Product, ProductVariant, ItemStock
from promotions.models import Coupon
from .models import Cart, CartItem


def get_or_create_cart(request):
    """Obtener o crear carrito para la sesión actual"""
    if not request.session.session_key:
        request.session.create()
    
    try:
        session = Session.objects.get(session_key=request.session.session_key)
        cart, created = Cart.objects.get_or_create(session=session)
    except Session.DoesNotExist:
        request.session.create()
        session = Session.objects.get(session_key=request.session.session_key)
        cart, created = Cart.objects.get_or_create(session=session)
    
    return cart


def cart_detail(request):
    """Vista del carrito de compras"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    # Obtener cupón aplicado de la sesión
    applied_coupon = None
    discount_amount = 0
    if 'applied_coupon_id' in request.session:
        try:
            applied_coupon = Coupon.objects.get(id=request.session['applied_coupon_id'])
            if applied_coupon.is_valid():
                # Calcular el descuento
                discount_amount = applied_coupon.calculate_discount(cart.get_total())
            else:
                # Si el cupón ya no es válido, removerlo de la sesión
                del request.session['applied_coupon_id']
                applied_coupon = None
        except Coupon.DoesNotExist:
            del request.session['applied_coupon_id']
    
    # Calcular el total final después del descuento
    final_total = cart.get_total() - discount_amount
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'applied_coupon': applied_coupon,
        'discount_amount': discount_amount,
        'final_total': final_total,
    }
    return render(request, 'cart/cart_detail.html', context)


@require_POST
def remove_cart_item(request, item_id):
    """Eliminar un item específico del carrito"""
    try:
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        # Liberar stock reservado
        if cart_item.variant:
            # Buscar stock de la variante
            try:
                stock_item = ItemStock.objects.get(product=cart_item.product, variant=cart_item.variant)
                stock_item.release_stock(cart_item.quantity)
            except ItemStock.DoesNotExist:
                pass
        else:
            # Buscar stock del producto sin variante
            try:
                stock_item = ItemStock.objects.get(product=cart_item.product, variant__isnull=True)
                stock_item.release_stock(cart_item.quantity)
            except ItemStock.DoesNotExist:
                pass
        
        # Eliminar el item del carrito
        product_name = cart_item.get_product_display_name()
        cart_item.delete()
        
        messages.success(request, f'{product_name} removido del carrito.')
        
    except Exception as e:
        messages.error(request, f'Error al remover el producto: {str(e)}')
    
    return redirect('cart:cart_detail')


@require_POST
def add_to_cart(request, product_id):
    """Agregar producto al carrito"""
    try:
        product = get_object_or_404(Product, id=product_id, is_active=True)
        quantity = int(request.POST.get('quantity', 1))
        variant_id = request.POST.get('variant_id')
        
        if quantity <= 0:
            messages.error(request, 'La cantidad debe ser mayor a 0.')
            return redirect(request.META.get('HTTP_REFERER', 'catalog:home'))
        
        # Obtener la variante si se especificó
        variant = None
        if variant_id:
            try:
                variant = ProductVariant.objects.get(id=variant_id, product=product, is_active=True)
            except ProductVariant.DoesNotExist:
                messages.error(request, 'La variante seleccionada no es válida.')
                return redirect(request.META.get('HTTP_REFERER', 'catalog:home'))
        
        # Verificar stock disponible
        try:
            if variant:
                stock_item = ItemStock.objects.get(product=product, variant=variant)
            else:
                stock_item = ItemStock.objects.get(product=product, variant__isnull=True)
            
            if stock_item.available_quantity < quantity:
                messages.error(request, f'Solo hay {stock_item.available_quantity} unidades disponibles.')
                return redirect(request.META.get('HTTP_REFERER', 'catalog:home'))
                
        except ItemStock.DoesNotExist:
            # Crear automáticamente un registro de stock si no existe
            try:
                stock_item = ItemStock.objects.create(
                    product=product,
                    variant=variant,
                    quantity=product.stock,
                    reserved_quantity=0,
                    min_stock_level=5,
                    location='Almacén Principal'
                )
                messages.info(request, f'Stock inicializado para {product.name}.')
            except Exception as e:
                messages.error(request, f'Error al inicializar stock: {str(e)}')
                return redirect(request.META.get('HTTP_REFERER', 'catalog:home'))
        
        try:
            cart = get_or_create_cart(request)
            
            # Buscar si ya existe el item en el carrito
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                variant=variant,
                defaults={'quantity': quantity, 'price': product.price}
            )
            
            if not created:
                # Verificar que la nueva cantidad total no exceda el stock
                total_quantity = cart_item.quantity + quantity
                if total_quantity > stock_item.available_quantity:
                    messages.error(request, f'Solo puedes agregar {stock_item.available_quantity - cart_item.quantity} unidades más.')
                    return redirect(request.META.get('HTTP_REFERER', 'catalog:home'))
                
                cart_item.quantity += quantity
                cart_item.save()
            
            # Reservar stock
            if not stock_item.reserve_stock(quantity):
                messages.error(request, 'No hay suficiente stock disponible.')
                return redirect(request.META.get('HTTP_REFERER', 'catalog:home'))
            
            messages.success(request, f'{cart_item.get_product_display_name()} agregado al carrito.')
            
            # Redirigir a la página anterior o a la página del producto
            referer = request.META.get('HTTP_REFERER')
            if referer:
                return redirect(referer)
            else:
                return redirect('catalog:product_detail', product_id=product_id)
                
        except Exception as e:
            messages.error(request, f'Error al agregar al carrito: {str(e)}')
            return redirect(request.META.get('HTTP_REFERER', 'catalog:home'))
                
    except Exception as e:
        messages.error(request, f'Error general: {str(e)}')
        return redirect('catalog:offers')


@require_POST
def update_cart_item(request, item_id):
    """Actualizar cantidad de un item en el carrito"""
    try:
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        new_quantity = int(request.POST.get('quantity', 1))
        old_quantity = cart_item.quantity
        
        if new_quantity <= 0:
            # Liberar stock reservado y eliminar item
            if cart_item.variant:
                try:
                    stock_item = ItemStock.objects.get(product=cart_item.product, variant=cart_item.variant)
                    stock_item.release_stock(old_quantity)
                except ItemStock.DoesNotExist:
                    pass
            else:
                try:
                    stock_item = ItemStock.objects.get(product=cart_item.product, variant__isnull=True)
                    stock_item.release_stock(old_quantity)
                except ItemStock.DoesNotExist:
                    pass
            
            product_name = cart_item.get_product_display_name()
            cart_item.delete()
            messages.success(request, f'{product_name} removido del carrito.')
        else:
            # Verificar stock disponible
            if cart_item.variant:
                stock_item = ItemStock.objects.get(product=cart_item.product, variant=cart_item.variant)
            else:
                stock_item = ItemStock.objects.get(product=cart_item.product, variant__isnull=True)
            
            # Calcular stock disponible considerando lo ya reservado
            available_stock = stock_item.quantity - (stock_item.reserved_quantity - old_quantity)
            
            if new_quantity > available_stock:
                messages.error(request, f'Solo hay {available_stock} unidades disponibles.')
            else:
                # Actualizar cantidad y stock reservado
                stock_item.release_stock(old_quantity)
                stock_item.reserve_stock(new_quantity)
                
                cart_item.quantity = new_quantity
                cart_item.save()
                
                messages.success(request, 'Carrito actualizado.')
    except Exception as e:
        messages.error(request, f'Error al actualizar el carrito: {str(e)}')
    
    return redirect('cart:cart_detail')





def clear_cart(request):
    """Limpiar todo el carrito"""
    cart = get_or_create_cart(request)
    
    # Liberar todo el stock reservado
    for item in cart.items.all():
        if item.variant:
            try:
                stock_item = ItemStock.objects.get(product=item.product, variant=item.variant)
                stock_item.release_stock(item.quantity)
            except ItemStock.DoesNotExist:
                pass
        else:
            try:
                stock_item = ItemStock.objects.get(product=item.product, variant__isnull=True)
                stock_item.release_stock(item.quantity)
            except ItemStock.DoesNotExist:
                pass
    
    cart.clear()
    messages.success(request, 'Carrito limpiado.')
    return redirect('cart:cart_detail')


def cart_count(request):
    """Obtener cantidad de items en el carrito (para AJAX)"""
    cart = get_or_create_cart(request)
    return JsonResponse({'count': cart.get_item_count()})


@require_POST
def apply_coupon(request):
    """Aplicar cupón de descuento"""
    coupon_code = request.POST.get('coupon_code', '').strip().upper()
    
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
            messages.error(request, f'El monto mínimo para usar este cupón es RD$ {coupon.min_amount}.')
            return redirect('cart:cart_detail')
        
        # Guardar el cupón en la sesión
        request.session['applied_coupon_id'] = coupon.id
        discount = coupon.calculate_discount(cart_total)
        
        messages.success(request, f'¡Cupón aplicado exitosamente! Descuento: RD$ {discount:.2f}')
        
    except Coupon.DoesNotExist:
        messages.error(request, 'El código de cupón ingresado no existe.')
    
    return redirect('cart:cart_detail')


@require_POST
def remove_coupon(request):
    """Remover cupón aplicado"""
    if 'applied_coupon_id' in request.session:
        del request.session['applied_coupon_id']
        messages.success(request, 'Cupón removido exitosamente.')
    else:
        messages.info(request, 'No hay cupón aplicado para remover.')
    
    return redirect('cart:cart_detail')
