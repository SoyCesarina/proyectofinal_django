// Funciones para el selector de cantidad
function incrementQuantity() {
    const quantityInput = document.getElementById('quantity');
    const currentValue = parseInt(quantityInput.value);
    const maxValue = parseInt(quantityInput.max);
    
    if (currentValue < maxValue) {
        quantityInput.value = currentValue + 1;
        updateButtonState();
    }
}

function decrementQuantity() {
    const quantityInput = document.getElementById('quantity');
    const currentValue = parseInt(quantityInput.value);
    const minValue = parseInt(quantityInput.min);
    
    if (currentValue > minValue) {
        quantityInput.value = currentValue - 1;
        updateButtonState();
    }
}

function updateButtonState() {
    const quantityInput = document.getElementById('quantity');
    const currentValue = parseInt(quantityInput.value);
    const maxValue = parseInt(quantityInput.max);
    const minValue = parseInt(quantityInput.min);
    
    const decrementBtn = quantityInput.parentElement.querySelector('button:first-child');
    const incrementBtn = quantityInput.parentElement.querySelector('button:last-child');
    
    // Actualizar estado de botones
    decrementBtn.disabled = currentValue <= minValue;
    incrementBtn.disabled = currentValue >= maxValue;
    
    // Actualizar clases CSS
    if (currentValue <= minValue) {
        decrementBtn.classList.add('disabled');
    } else {
        decrementBtn.classList.remove('disabled');
    }
    
    if (currentValue >= maxValue) {
        incrementBtn.classList.add('disabled');
    } else {
        incrementBtn.classList.remove('disabled');
    }
}

// Función para cambiar la imagen principal
function changeMainImage(imageSrc) {
    const mainImage = document.getElementById('mainImage');
    if (mainImage) {
        // Efecto de fade out
        mainImage.style.opacity = '0';
        
        setTimeout(() => {
            mainImage.src = imageSrc;
            // Efecto de fade in
            mainImage.style.opacity = '1';
        }, 150);
    }
    
    // Actualizar estado activo de las miniaturas
    const thumbnails = document.querySelectorAll('.thumbnail');
    thumbnails.forEach(thumb => {
        if (thumb.src === imageSrc) {
            thumb.classList.add('active');
        } else {
            thumb.classList.remove('active');
        }
    });
}

// Función para agregar producto al carrito desde productos relacionados
function addRelatedProductToCart(productId, event) {
    event.preventDefault();
    
    const form = event.target;
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
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Mostrar mensaje de éxito
            showNotification('Producto agregado al carrito', 'success');
            
            // Actualizar contador del carrito
            updateCartCount(data.cart_count);
            
            // Cambiar botón a estado de éxito
            submitBtn.innerHTML = '<i class="fas fa-check me-2"></i>¡Agregado!';
            submitBtn.classList.remove('btn-accent');
            submitBtn.classList.add('btn-success');
            
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
                submitBtn.classList.remove('btn-success');
                submitBtn.classList.add('btn-accent');
            }, 2000);
        } else {
            showNotification('Error al agregar el producto', 'error');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error al agregar el producto', 'error');
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    });
}

// Función para mostrar notificaciones
function showNotification(message, type = 'info') {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'success' ? 'success' : type === 'error' ? 'danger' : 'info'} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Agregar al DOM
    document.body.appendChild(notification);
    
    // Remover automáticamente después de 3 segundos
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 3000);
}

// Función para actualizar contador del carrito
function updateCartCount(count) {
    const cartBadge = document.getElementById('cart-count');
    if (cartBadge) {
        cartBadge.textContent = count;
        
        // Efecto de animación
        cartBadge.style.transform = 'scale(1.2)';
        setTimeout(() => {
            cartBadge.style.transform = 'scale(1)';
        }, 200);
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar estado de botones de cantidad
    updateButtonState();
    
    // Agregar validación al input de cantidad
    const quantityInput = document.getElementById('quantity');
    if (quantityInput) {
        quantityInput.addEventListener('input', function() {
            const value = parseInt(this.value);
            const max = parseInt(this.max);
            const min = parseInt(this.min);
            
            if (value > max) {
                this.value = max;
            } else if (value < min) {
                this.value = min;
            }
            
            updateButtonState();
        });
    }
    
    // Configurar formularios de productos relacionados
    const relatedProductForms = document.querySelectorAll('form[action*="add_to_cart"]');
    relatedProductForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            addRelatedProductToCart(null, event);
        });
    });
    
    // Configurar miniaturas de imágenes
    const thumbnails = document.querySelectorAll('.thumbnail');
    thumbnails.forEach(thumb => {
        thumb.addEventListener('click', function() {
            changeMainImage(this.src);
        });
    });
    
    // Efecto de hover en las cards de productos relacionados
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Animación de entrada para productos relacionados
    const relatedProducts = document.querySelectorAll('.related-products .product-card');
    relatedProducts.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});
