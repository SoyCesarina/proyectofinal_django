// Actualizar contador del carrito
function updateCartCount() {
    const cartCountElement = document.getElementById('cart-count');
    if (!cartCountElement) {
        console.warn('Elemento cart-count no encontrado');
        return;
    }
    
    fetch('/cart/count/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data && typeof data.count !== 'undefined') {
                cartCountElement.textContent = data.count;
                console.log('Contador del carrito actualizado:', data.count);
            } else {
                console.warn('Respuesta inválida del servidor:', data);
            }
        })
        .catch(error => {
            console.error('Error al actualizar contador del carrito:', error);
            // Mantener el contador en 0 si hay error
            cartCountElement.textContent = '0';
        });
}

// Función para forzar la actualización del contador
function forceUpdateCartCount() {
    console.log('Forzando actualización del contador del carrito...');
    updateCartCount();
}

// Actualizar contador al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM cargado, actualizando contador del carrito...');
    updateCartCount();
    
    // También actualizar después de un pequeño delay para asegurar que todo esté listo
    setTimeout(updateCartCount, 100);
});

// Actualizar contador cuando la página se vuelve visible (útil para pestañas)
document.addEventListener('visibilitychange', function() {
    if (!document.hidden) {
        console.log('Página visible, actualizando contador del carrito...');
        updateCartCount();
    }
});
