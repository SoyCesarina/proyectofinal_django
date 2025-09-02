// Función para incrementar cantidad
function incrementQuantity(itemId) {
    const quantityInput = document.getElementById('quantity-' + itemId);
    const currentValue = parseInt(quantityInput.value);
    
    // Incrementar la cantidad
    quantityInput.value = currentValue + 1;
    
    // Actualizar estado de botones
    updateButtonState(itemId);
    
    // Actualizar automáticamente después de un breve delay
    setTimeout(() => {
        autoUpdateQuantity(itemId);
    }, 500);
}

// Función para decrementar cantidad
function decrementQuantity(itemId) {
    const quantityInput = document.getElementById('quantity-' + itemId);
    const currentValue = parseInt(quantityInput.value);
    const minValue = parseInt(quantityInput.min);
    
    if (currentValue > minValue) {
        quantityInput.value = currentValue - 1;
        
        // Actualizar estado de botones
        updateButtonState(itemId);
        
        // Actualizar automáticamente después de un breve delay
        setTimeout(() => {
            autoUpdateQuantity(itemId);
        }, 500);
    }
}

// Función para actualizar el estado de los botones
function updateButtonState(itemId) {
    const quantityInput = document.getElementById('quantity-' + itemId);
    const currentValue = parseInt(quantityInput.value);
    const minValue = parseInt(quantityInput.min);
    
    // Obtener los botones del selector de cantidad
    const quantitySelector = quantityInput.closest('.quantity-selector');
    const decrementBtn = quantitySelector.querySelector('button:first-child');
    const incrementBtn = quantitySelector.querySelector('button:last-child');
    
    // Actualizar estado de botones
    decrementBtn.disabled = currentValue <= minValue;
    incrementBtn.disabled = false; // No limitamos el incremento por ahora
    
    // Actualizar clases CSS para mejor feedback visual
    if (currentValue <= minValue) {
        decrementBtn.classList.add('btn-secondary');
        decrementBtn.classList.remove('btn-outline-secondary');
    } else {
        decrementBtn.classList.remove('btn-secondary');
        decrementBtn.classList.add('btn-outline-secondary');
    }
}

// Función para actualizar automáticamente la cantidad
function autoUpdateQuantity(itemId) {
    const quantityInput = document.getElementById('quantity-' + itemId);
    const form = quantityInput.closest('form');
    
    if (form) {
        // Mostrar indicador de carga en el botón de actualizar
        const submitBtn = form.querySelector('button[type="submit"]');
        
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        submitBtn.disabled = true;
        submitBtn.classList.add('btn-primary');
        submitBtn.classList.remove('btn-outline-primary');
        
        // Enviar el formulario
        form.submit();
    }
}

// Inicializar cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    // Obtener todos los selectores de cantidad en el carrito
    const quantityInputs = document.querySelectorAll('[id^="quantity-"]');
    
    quantityInputs.forEach(function(input) {
        const itemId = input.id.split('-')[1];
        
        // Inicializar estado de botones
        updateButtonState(itemId);
        
        // Agregar validación al input
        input.addEventListener('input', function() {
            const value = parseInt(this.value);
            const min = parseInt(this.min);
            
            if (value < min) {
                this.value = min;
            }
            
            updateButtonState(itemId);
        });
        
        // Agregar evento para actualizar cuando se presiona Enter
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                autoUpdateQuantity(itemId);
            }
        });
        
        // Agregar evento para actualizar cuando se pierde el foco
        input.addEventListener('blur', function() {
            setTimeout(() => {
                autoUpdateQuantity(itemId);
            }, 100);
        });
    });
});
