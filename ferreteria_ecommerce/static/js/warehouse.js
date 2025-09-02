// Función simple para manejar filtros
function handleFilter(filter) {
    console.log('Handling filter:', filter);
    
    // Obtener la URL actual
    let url = new URL(window.location);
    
    // Obtener la página actual
    let currentPage = url.searchParams.get('page');
    
    // Limpiar parámetros existentes
    url.searchParams.delete('status');
    url.searchParams.delete('page');
    
    // Si no es "all", agregar el filtro de estado
    if (filter !== 'all') {
        url.searchParams.set('status', filter);
    }
    
    // Mantener la página actual si existe
    if (currentPage) {
        url.searchParams.set('page', currentPage);
    }
    
    console.log('Navigating to:', url.toString());
    
    // Navegar a la nueva URL
    window.location.href = url.toString();
}

// Configurar los botones cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    console.log('Setting up filter buttons...');
    
    // Obtener todos los botones de filtro
    const buttons = document.querySelectorAll('button[data-filter]');
    console.log('Found buttons:', buttons.length);
    
    // Agregar event listener a cada botón
    buttons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const filter = this.getAttribute('data-filter');
            console.log('Button clicked:', filter);
            
            // Mostrar indicador de carga en el botón
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Cargando...';
            this.disabled = true;
            
            // Aplicar el filtro
            handleFilter(filter);
        });
    });
    
    // Configurar el modal de eliminación de todas las órdenes
    const deleteAllModal = document.getElementById('deleteAllOrdersModal');
    const confirmDeleteBtn = document.getElementById('confirmDeleteAllBtn');
    
    if (deleteAllModal && confirmDeleteBtn) {
        // Cuando se abre el modal, actualizar el contador
        deleteAllModal.addEventListener('show.bs.modal', function() {
            const orderCount = document.querySelector('.badge.bg-secondary.fs-6.me-3').textContent.split(': ')[1].split(' ')[0];
            const orderCountElement = this.querySelector('.alert ul li:first-child');
            if (orderCountElement) {
                orderCountElement.textContent = `Todas las órdenes del sistema (${orderCount} órdenes)`;
            }
        });
        
        // Cuando se confirma la eliminación, mostrar indicador de carga y enviar el formulario
        confirmDeleteBtn.addEventListener('click', function(e) {
            // Prevenir el comportamiento por defecto del botón
            e.preventDefault();
            
            console.log('DEBUG: Botón de confirmar eliminación clickeado');
            
            // Mostrar indicador de carga
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Eliminando...';
            this.disabled = true;
            
            // Cerrar el modal
            const modal = bootstrap.Modal.getInstance(deleteAllModal);
            if (modal) {
                modal.hide();
            }
            
            // Enviar el formulario manualmente
            const form = this.closest('form');
            if (form) {
                console.log('DEBUG: Enviando formulario...');
                form.submit();
            } else {
                console.error('DEBUG: No se encontró el formulario');
            }
        });
    }
    
    console.log('Filter buttons setup complete');
});
