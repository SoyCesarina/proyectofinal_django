from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.http import HttpResponse
from .models import Category, Product, ProductImage


def home(request):
    """Vista de la página de inicio"""
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:8]
    categories = Category.objects.filter(is_active=True, parent=None)[:6]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'catalog/home.html', context)


def product_list(request):
    """Lista de productos con filtros"""
    products = Product.objects.filter(is_active=True)
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = products.filter(category=category)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Ordenamiento - por defecto mostrar los más recientes primero
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:  # newest por defecto
        products = products.order_by('-created_at')
    
    # Paginación
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'catalog/product_list.html', context)


def offers(request):
    """Vista para mostrar ofertas destacadas (productos con descuento)"""
    # Filtro por categoría
    category_slug = request.GET.get('category')
    current_category = None
    
    if category_slug:
        # Si se selecciona una categoría específica, mostrar todos los productos de esa categoría
        current_category = category_slug
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = Product.objects.filter(category=category, is_active=True)
    else:
        # Si no se selecciona categoría (Todas las Ofertas), mostrar solo productos con descuento
        products = Product.objects.filter(
            is_active=True,
            is_featured=True,
            original_price__isnull=False,
            original_price__gt=F('price')
        )
    
    # Búsqueda
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Ordenamiento
    sort_by = request.GET.get('sort', 'newest' if category_slug else 'discount')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'discount' and not category_slug:
        # Solo aplicar ordenamiento por descuento si no hay categoría seleccionada
        products = products.annotate(
            discount_percentage=((F('original_price') - F('price')) / F('original_price') * 100)
        ).order_by('-discount_percentage', '-created_at')
    else:
        # Por defecto, ordenar por más recientes
        products = products.order_by('-created_at')
    
    # Paginación
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': current_category,
        'search_query': search_query,
        'sort_by': sort_by,
        'is_offers_page': True,
    }
    
    # Si se selecciona una categoría específica, usar el template de product_list
    if category_slug:
        return render(request, 'catalog/product_list.html', context)
    else:
        # Si no hay categoría seleccionada (Todas las Ofertas), usar el template de offers
        return render(request, 'catalog/offers.html', context)


def product_detail(request, slug):
    """Detalle de un producto"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Obtener productos relacionados de la misma categoría
    same_category_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:3]
    
    # Obtener productos destacados de otras categorías
    featured_products = Product.objects.filter(
        is_featured=True,
        is_active=True
    ).exclude(id=product.id).exclude(category=product.category)[:2]
    
    # Combinar productos relacionados
    related_products = list(same_category_products) + list(featured_products)
    
    # Si no hay suficientes productos relacionados, agregar productos recientes
    if len(related_products) < 4:
        recent_products = Product.objects.filter(
            is_active=True
        ).exclude(id=product.id).exclude(id__in=[p.id for p in related_products])[:4-len(related_products)]
        related_products.extend(recent_products)
    
    # Limitar a 4 productos
    related_products = related_products[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'catalog/product_detail.html', context)


def category_detail(request, slug):
    """Detalle de una categoría"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, is_active=True)
    
    # Búsqueda dentro de la categoría
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Ordenamiento - por defecto mostrar los más recientes primero
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:  # newest por defecto
        products = products.order_by('-created_at')
    
    # Paginación
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'catalog/category_detail.html', context)


def product_image(request, image_id):
    """Vista para servir imágenes desde la base de datos"""
    try:
        product_image = get_object_or_404(ProductImage, id=image_id)
        response = HttpResponse(product_image.image_data, content_type=product_image.image_type)
        response['Content-Disposition'] = f'inline; filename="{product_image.filename}"'
        return response
    except Exception as e:
        # Retornar una imagen por defecto o error 404
        return HttpResponse(status=404)
