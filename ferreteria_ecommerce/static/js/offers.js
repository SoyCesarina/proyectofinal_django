// JavaScript para la página de ofertas
// Esperar a que base.js esté completamente cargado
function initializeOffers() {
    
    // Asegurar que el contador del carrito se actualice
    if (typeof updateCartCount === 'function') {
        console.log('Actualizando contador del carrito desde offers.js...');
        updateCartCount();
    } else {
        console.warn('Función updateCartCount no encontrada, esperando...');
        // Reintentar después de un delay
        setTimeout(initializeOffers, 100);
        return;
    }
    
    // Función para agregar producto al carrito con mejor UX
    function addToCart(form) {
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
    
        // Mostrar estado de carga
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Agregando...';
        submitBtn.disabled = true;
    
        // Enviar formulario
        fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
            headers: {
                'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => {
            if (response.redirected) {
                // Si hay redirección, seguirla
                window.location.href = response.url;
            } else {
                // Si no hay redirección, recargar la página para mostrar mensajes
                window.location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Restaurar botón en caso de error
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
            
            // Mostrar mensaje de error
            showNotification('Error al agregar el producto', 'error');
        });
    }
    
    // Configurar todos los formularios de agregar al carrito
    const addToCartForms = document.querySelectorAll('form[action*="add_to_cart"]');
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            addToCart(this);
        });
    });
    
    // Función para mostrar notificaciones
    function showNotification(message, type = 'info') {
        // Crear elemento de notificación
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            <i class="fas fa-${type === 'error' ? 'exclamation-circle' : type === 'success' ? 'check-circle' : 'info-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        // Agregar al body
        document.body.appendChild(notification);
        
        // Auto-ocultar después de 5 segundos
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }


    
    // Efectos hover mejorados para las cards
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
            this.style.boxShadow = '0 8px 25px rgba(0,0,0,0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 15px rgba(0,0,0,0.1)';
        });
    });
    
    // Animación de entrada para productos
    const productItems = document.querySelectorAll('.col-xl-2, .col-lg-3, .col-md-4, .col-sm-6');
    productItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            item.style.transition = 'all 0.6s ease';
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Mejorar la funcionalidad de búsqueda
    const searchForm = document.querySelector('form[method="GET"]');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="q"]');
        const searchButton = searchForm.querySelector('button[type="submit"]');
        
        // Búsqueda en tiempo real (opcional)
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.value.length >= 3) {
                    // Auto-enviar búsqueda después de 3 caracteres
                    searchForm.submit();
                }
            }, 1000);
        });
        
        // Efecto visual en el botón de búsqueda
        searchButton.addEventListener('click', function() {
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            setTimeout(() => {
                this.innerHTML = '<i class="fas fa-search"></i>';
            }, 1000);
        });
    }
    
    // Mejorar la funcionalidad de filtros
    const categoryItems = document.querySelectorAll('.category-item');
    categoryItems.forEach(item => {
        item.addEventListener('click', function() {
            // Efecto visual al hacer clic
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });
    
    // Lazy loading para imágenes (opcional)
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        imageObserver.unobserve(img);
                    }
                }
        });
    });
        
        const images = document.querySelectorAll('img[data-src]');
        images.forEach(img => imageObserver.observe(img));
    }
    
    // Mejorar la accesibilidad
    const buttons = document.querySelectorAll('button, a[role="button"]');
    buttons.forEach(button => {
        button.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                this.click();
            }
        });
    });
    
    // Mostrar mensajes de Django si existen
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        // Auto-ocultar mensajes después de 5 segundos
        setTimeout(() => {
            if (message.parentNode) {
                message.remove();
            }
        }, 5000);
        
        // Efecto de entrada
        message.style.opacity = '0';
        message.style.transform = 'translateY(-20px)';
        
        setTimeout(() => {
            message.style.transition = 'all 0.5s ease';
            message.style.opacity = '1';
            message.style.transform = 'translateY(0)';
        }, 100);
    });
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM cargado en offers.js, inicializando...');
    initializeOffers();
});

// También inicializar si la función ya está disponible
if (typeof updateCartCount === 'function') {
    console.log('updateCartCount ya disponible, inicializando inmediatamente...');
    initializeOffers();
}
