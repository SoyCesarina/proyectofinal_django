from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.urls import reverse
from django.db import transaction
from .models import InventoryMovement, Shipment
from orders.models import Order


def redirect_with_params(request, url_name):
    """Redirigir manteniendo los parámetros de filtro y página"""
    # Obtener parámetros actuales
    status_filter = request.GET.get('status')
    page = request.GET.get('page')
    
    # Construir la URL base
    url = reverse(url_name)
    
    # Agregar parámetros si existen
    params = []
    if status_filter:
        params.append(f'status={status_filter}')
    if page:
        params.append(f'page={page}')
    
    # Construir URL final
    if params:
        url += '?' + '&'.join(params)
    
    return redirect(url)


def order_list(request):
    """Lista de órdenes para el almacén"""
    # Mostrar todas las órdenes ordenadas por fecha y hora de creación (más recientes primero)
    orders = Order.objects.select_related('coupon').order_by('-created_at', '-id')
    
    # Filtros
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    # Paginación
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
    }
    return render(request, 'warehouse/order_list.html', context)


def order_detail_warehouse(request, order_number):
    """Detalle de orden para el almacén"""
    order = get_object_or_404(Order, order_number=order_number)
    
    context = {
        'order': order,
    }
    return render(request, 'warehouse/order_detail.html', context)


@require_POST
def ship_order(request, order_number):
    """Despachar una orden"""
    print(f"DEBUG: Despachando orden {order_number}")
    
    try:
        # Buscar la orden
        order = Order.objects.get(order_number=order_number, status='ready_to_ship')
        print(f"DEBUG: Orden encontrada: {order.order_number}")
        
        # Crear el despacho con valores por defecto
        shipment = Shipment.objects.create(
            order=order,
            tracking_number='',  # Vacío por defecto
            carrier='Sin especificar',  # Valor por defecto
            notes='Despachado automáticamente'  # Nota por defecto
        )
        
        print(f"DEBUG: Despacho creado exitosamente - ID: {shipment.id}")
        messages.success(request, f'Orden {order.order_number} despachada exitosamente.')
        
    except Order.DoesNotExist:
        print(f"DEBUG: Orden no encontrada o no está lista para despachar")
        messages.error(request, 'La orden no existe o no está lista para despachar.')
    except Exception as e:
        print(f"DEBUG: Error inesperado: {str(e)}")
        messages.error(request, 'Error al procesar el despacho. Intente nuevamente.')
    
    # Preservar parámetros de filtro y página
    return redirect_with_params(request, 'warehouse:order_list')


@require_POST
def confirm_order(request, order_number):
    """Confirmar una orden pendiente"""
    order = get_object_or_404(Order, order_number=order_number, status='pending')
    
    order.status = 'confirmed'
    order.save()
    
    messages.success(request, f'Orden {order.order_number} confirmada exitosamente.')
    # Preservar parámetros de filtro y página
    return redirect_with_params(request, 'warehouse:order_list')


@require_POST
def mark_ready_to_ship(request, order_number):
    """Marcar orden como lista para despachar"""
    order = get_object_or_404(Order, order_number=order_number, status='confirmed')
    
    order.status = 'ready_to_ship'
    order.save()
    
    messages.success(request, f'Orden {order.order_number} marcada como lista para despachar.')
    # Preservar parámetros de filtro y página
    return redirect_with_params(request, 'warehouse:order_list')


@require_POST
def mark_delivered(request, order_number):
    """Marcar orden como entregada"""
    print(f"DEBUG: Marcando orden {order_number} como entregada")
    
    try:
        order = Order.objects.get(order_number=order_number, status='shipped')
        print(f"DEBUG: Orden encontrada: {order.order_number}")
        
        order.status = 'delivered'
        order.save()
        
        print(f"DEBUG: Orden marcada como entregada exitosamente")
        messages.success(request, f'Orden {order.order_number} marcada como entregada.')
        
    except Order.DoesNotExist:
        print(f"DEBUG: Orden no encontrada o no está despachada")
        messages.error(request, 'La orden no existe o no está despachada.')
    except Exception as e:
        print(f"DEBUG: Error inesperado: {str(e)}")
        messages.error(request, 'Error al marcar la orden como entregada.')
    
    # Preservar parámetros de filtro y página
    return redirect_with_params(request, 'warehouse:order_list')


@require_POST
@transaction.atomic
def delete_all_orders(request):
    """Eliminar todas las órdenes del sistema"""
    print(f"DEBUG: Función delete_all_orders llamada")
    print(f"DEBUG: Método de la solicitud: {request.method}")
    
    try:
        # Contar órdenes antes de eliminar
        total_orders = Order.objects.count()
        print(f"DEBUG: Total de órdenes a eliminar: {total_orders}")
        
        if total_orders == 0:
            print(f"DEBUG: No hay órdenes para eliminar")
            messages.warning(request, 'No hay órdenes para eliminar.')
            return redirect('warehouse:order_list')
        
        # Eliminar todas las órdenes (esto también eliminará OrderItems por CASCADE)
        print(f"DEBUG: Eliminando {total_orders} órdenes...")
        Order.objects.all().delete()
        print(f"DEBUG: Órdenes eliminadas exitosamente")
        
        # También eliminar movimientos de inventario y despachos relacionados
        print(f"DEBUG: Eliminando movimientos de inventario...")
        inventory_count = InventoryMovement.objects.count()
        InventoryMovement.objects.all().delete()
        print(f"DEBUG: {inventory_count} movimientos de inventario eliminados")
        
        print(f"DEBUG: Eliminando despachos...")
        shipment_count = Shipment.objects.count()
        Shipment.objects.all().delete()
        print(f"DEBUG: {shipment_count} despachos eliminados")
        
        print(f"DEBUG: Proceso de eliminación completado exitosamente")
        messages.success(request, f'Se eliminaron exitosamente {total_orders} órdenes y todos los registros relacionados.')
        
    except Exception as e:
        print(f"DEBUG: Error al eliminar las órdenes: {str(e)}")
        messages.error(request, f'Error al eliminar las órdenes: {str(e)}')
    
    print(f"DEBUG: Redirigiendo a order_list")
    return redirect('warehouse:order_list')


def inventory_movements(request):
    """Lista de movimientos de inventario"""
    movements = InventoryMovement.objects.all().order_by('-created_at')
    
    # Filtros
    movement_type = request.GET.get('type')
    if movement_type:
        movements = movements.filter(movement_type=movement_type)
    
    # Paginación
    paginator = Paginator(movements, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'movement_type': movement_type,
    }
    return render(request, 'warehouse/inventory_movements.html', context)


def shipments_list(request):
    """Lista de despachos"""
    shipments = Shipment.objects.all().order_by('-shipped_at')
    
    # Paginación
    paginator = Paginator(shipments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'warehouse/shipments_list.html', context)
