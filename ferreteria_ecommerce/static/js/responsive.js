// Responsive Design JavaScript - Ferretería E-commerce

document.addEventListener('DOMContentLoaded', function() {
    
    // ===== DETECCIÓN DE ZOOM Y DPI =====
    
    // Función para detectar el nivel de zoom actual
    function getZoomLevel() {
        return window.devicePixelRatio || 1;
    }
    
    // Función para detectar la resolución de pantalla
    function getScreenResolution() {
        return window.screen.width * window.devicePixelRatio;
    }
    
    // Función para aplicar clases CSS basadas en el zoom
    function applyZoomClasses() {
        const zoomLevel = getZoomLevel();
        const body = document.body;
        
        // Remover clases anteriores
        body.classList.remove('zoom-low', 'zoom-normal', 'zoom-high', 'zoom-extreme');
        
        // Aplicar clase basada en el nivel de zoom
        if (zoomLevel < 0.9) {
            body.classList.add('zoom-low');
        } else if (zoomLevel >= 0.9 && zoomLevel <= 1.1) {
            body.classList.add('zoom-normal');
        } else if (zoomLevel > 1.1 && zoomLevel <= 1.5) {
            body.classList.add('zoom-high');
        } else if (zoomLevel > 1.5) {
            body.classList.add('zoom-extreme');
        }
    }
    
    // ===== MANEJO DE ORIENTACIÓN =====
    
    // Función para manejar cambios de orientación
    function handleOrientationChange() {
        const isLandscape = window.innerHeight < window.innerWidth;
        const body = document.body;
        
        if (isLandscape && window.innerHeight < 500) {
            body.classList.add('landscape-mobile');
        } else {
            body.classList.remove('landscape-mobile');
        }
    }
    
    // ===== MANEJO DE TAMAÑO DE PANTALLA =====
    
    // Función para aplicar clases de tamaño de pantalla
    function applyScreenSizeClasses() {
        const width = window.innerWidth;
        const body = document.body;
        
        // Remover clases anteriores
        body.classList.remove('screen-xs', 'screen-sm', 'screen-md', 'screen-lg', 'screen-xl', 'screen-xxl');
        
        // Aplicar clase basada en el ancho de pantalla
        if (width < 576) {
            body.classList.add('screen-xs');
        } else if (width >= 576 && width < 768) {
            body.classList.add('screen-sm');
        } else if (width >= 768 && width < 992) {
            body.classList.add('screen-md');
        } else if (width >= 992 && width < 1200) {
            body.classList.add('screen-lg');
        } else if (width >= 1200 && width < 1400) {
            body.classList.add('screen-xl');
        } else {
            body.classList.add('screen-xxl');
        }
    }
    
    // ===== MANEJO DE TABLAS RESPONSIVAS =====
    
    // Función para hacer las tablas más responsivas
    function enhanceTableResponsiveness() {
        const tables = document.querySelectorAll('.table');
        
        tables.forEach(table => {
            if (!table.parentElement.classList.contains('table-responsive')) {
                const wrapper = document.createElement('div');
                wrapper.className = 'table-responsive';
                table.parentNode.insertBefore(wrapper, table);
                wrapper.appendChild(table);
            }
        });
    }
    
    // ===== MANEJO DE FORMULARIOS RESPONSIVOS =====
    
    // Función para mejorar la responsividad de formularios
    function enhanceFormResponsiveness() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, select, textarea');
            
            inputs.forEach(input => {
                // Agregar clases responsivas
                if (window.innerWidth < 768) {
                    input.classList.add('form-control-sm');
                } else {
                    input.classList.remove('form-control-sm');
                }
            });
        });
    }
    
    // ===== MANEJO DE NAVEGACIÓN RESPONSIVA =====
    
    // Función para mejorar la navegación en móviles
    function enhanceMobileNavigation() {
        const navbarToggler = document.querySelector('.navbar-toggler');
        const navbarCollapse = document.querySelector('.navbar-collapse');
        
        if (navbarToggler && navbarCollapse) {
            // Cerrar menú al hacer clic en un enlace en móviles
            const navLinks = navbarCollapse.querySelectorAll('.nav-link');
            
            navLinks.forEach(link => {
                link.addEventListener('click', () => {
                    if (window.innerWidth < 992) {
                        navbarCollapse.classList.remove('show');
                    }
                });
            });
        }
    }
    
    // ===== MANEJO DE IMÁGENES RESPONSIVAS =====
    
    // Función para optimizar imágenes según el zoom
    function optimizeImagesForZoom() {
        const images = document.querySelectorAll('img');
        const zoomLevel = getZoomLevel();
        
        images.forEach(img => {
            if (zoomLevel > 1.5) {
                img.style.imageRendering = 'crisp-edges';
            } else {
                img.style.imageRendering = 'auto';
            }
        });
    }
    
    // ===== MANEJO DE ACCESIBILIDAD =====
    
    // Función para mejorar la accesibilidad del teclado
    function enhanceKeyboardAccessibility() {
        // Agregar soporte para navegación con teclado
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });
        
        document.addEventListener('mousedown', function() {
            document.body.classList.remove('keyboard-navigation');
        });
    }
    
    // ===== MANEJO DE PERFORMANCE =====
    
    // Función para optimizar el rendimiento en dispositivos lentos
    function optimizeForSlowDevices() {
        const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
        
        if (connection && (connection.effectiveType === 'slow-2g' || connection.effectiveType === '2g')) {
            document.body.classList.add('slow-connection');
            
            // Reducir animaciones
            const style = document.createElement('style');
            style.textContent = `
                * {
                    animation-duration: 0.1s !important;
                    transition-duration: 0.1s !important;
                }
            `;
            document.head.appendChild(style);
        }
    }
    
    // ===== MANEJO DE EVENTOS =====
    
    // Aplicar todas las funciones al cargar la página
    function initializeResponsiveness() {
        applyZoomClasses();
        handleOrientationChange();
        applyScreenSizeClasses();
        enhanceTableResponsiveness();
        enhanceFormResponsiveness();
        enhanceMobileNavigation();
        optimizeImagesForZoom();
        enhanceKeyboardAccessibility();
        optimizeForSlowDevices();
    }
    
    // Event listeners para cambios de tamaño y zoom
    window.addEventListener('resize', function() {
        handleOrientationChange();
        applyScreenSizeClasses();
        enhanceFormResponsiveness();
    });
    
    // Detectar cambios de zoom (no es 100% confiable en todos los navegadores)
    let currentZoom = getZoomLevel();
    setInterval(() => {
        const newZoom = getZoomLevel();
        if (Math.abs(newZoom - currentZoom) > 0.1) {
            currentZoom = newZoom;
            applyZoomClasses();
            optimizeImagesForZoom();
        }
    }, 1000);
    
    // Event listener para cambios de orientación
    window.addEventListener('orientationchange', function() {
        setTimeout(handleOrientationChange, 100);
    });
    
    // Event listener para cambios de DPI (cuando cambia la ventana entre monitores)
    window.addEventListener('focus', function() {
        applyZoomClasses();
        optimizeImagesForZoom();
    });
    
    // ===== INICIALIZACIÓN =====
    
    // Inicializar cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeResponsiveness);
    } else {
        initializeResponsiveness();
    }
    
    // ===== FUNCIONES UTILITARIAS =====
    
    // Función para obtener el tamaño de pantalla en formato legible
    window.getScreenInfo = function() {
        return {
            width: window.innerWidth,
            height: window.innerHeight,
            zoom: getZoomLevel(),
            dpi: window.devicePixelRatio,
            orientation: window.innerHeight > window.innerWidth ? 'portrait' : 'landscape'
        };
    };
    
    // Función para forzar un reflow (útil para problemas de layout)
    window.forceReflow = function() {
        document.body.offsetHeight;
    };
    
    // Función para detectar si el dispositivo es táctil
    window.isTouchDevice = function() {
        return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    };
    
    // Función para detectar si el dispositivo es móvil
    window.isMobileDevice = function() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    };
    
    // ===== MANEJO DE ERRORES =====
    
    // Capturar errores de JavaScript relacionados con responsividad
    window.addEventListener('error', function(e) {
        if (e.message.includes('responsive') || e.message.includes('zoom')) {
            console.warn('Error de responsividad detectado:', e.message);
            // Intentar recuperar el estado
            setTimeout(initializeResponsiveness, 100);
        }
    });
    
    // ===== LOGGING PARA DEBUG =====
    
    // Solo en modo desarrollo
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        console.log('Responsive Design inicializado');
        console.log('Información de pantalla:', window.getScreenInfo());
    }
});

// ===== FUNCIONES GLOBALES =====

// Función para recargar la responsividad manualmente
window.reloadResponsiveness = function() {
    location.reload();
};

// Función para cambiar el zoom programáticamente (experimental)
window.setZoomLevel = function(level) {
    if (level >= 0.25 && level <= 5) {
        document.body.style.zoom = level;
        document.body.style.transform = `scale(${level})`;
        document.body.style.transformOrigin = 'top left';
    }
};
