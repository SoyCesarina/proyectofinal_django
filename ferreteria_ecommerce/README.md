# Ferretería E-commerce - Sistema de Gestión Completo

## Descripción del Proyecto

Sistema de e-commerce completo para ferretería desarrollado en Django que incluye gestión de catálogo, carrito de compras, órdenes, inventario y promociones. El proyecto está diseñado para manejar productos con variantes, control de stock, cupones de descuento y gestión de envíos.

## Características Principales

- **Catálogo de Productos**: Gestión completa de productos con categorías jerárquicas
- **Sistema de Variantes**: Productos con diferentes opciones (color, tamaño, etc.)
- **Carrito de Compras**: Basado en sesiones con persistencia en base de datos
- **Gestión de Órdenes**: Flujo completo desde checkout hasta entrega
- **Control de Inventario**: Movimientos de stock y gestión de bodega
- **Sistema de Promociones**: Cupones de descuento configurables
- **Panel de Administración**: Interfaz Django Admin personalizada
- **Responsive Design**: Interfaz adaptativa para diferentes dispositivos

## Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone [URL_DEL_REPOSITORIO]
cd ferreteria_ecommerce
```

### 2. Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv entornovirtual

# Activar entorno virtual (Windows)
entornovirtual\Scripts\activate

# Activar entorno virtual (Linux/Mac)
source entornovirtual/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos PostgreSQL

```sql
-- Crear base de datos
CREATE DATABASE django2proyecto;

-- Crear usuario (opcional)
CREATE USER postgres WITH PASSWORD '5102';
GRANT ALL PRIVILEGES ON DATABASE django2proyecto TO postgres;
```

### 5. Configurar Variables de Entorno

Crear el archivo `.env` en la raíz del proyecto:

```env
DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_NAME=django2proyecto
DATABASE_USER=postgres
DATABASE_PASSWORD=5102
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### 6. Ejecutar Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crear Superusuario

```bash
python manage.py createsuperuser
```

### 8. Cargar Datos de Ejemplo

```bash
# Poblar base de datos con productos y categorías
python manage.py populate_database

# Crear cupones de ejemplo
python manage.py create_coupons

# Crear imágenes de productos
python manage.py populate_product_media
```

### 9. Ejecutar el Servidor

```bash
python manage.py runserver
```

El proyecto estará disponible en: http://127.0.0.1:8000/

## Estructura del Proyecto y Archivos

### **ferreteria_ecommerce/** (Configuración Principal)
- **`settings.py`**: Configuración principal de Django (base de datos, middleware, apps instaladas)
- **`urls.py`**: URLs principales del proyecto que enrutan a las diferentes aplicaciones
- **`wsgi.py`**: Configuración WSGI para despliegue en producción
- **`asgi.py`**: Configuración ASGI para aplicaciones asíncronas

### **catalog/** (Gestión de Productos)
- **`models.py`**: Modelos de datos para productos, categorías, variantes e inventario
  - `Category`: Categorías jerárquicas de productos
  - `Product`: Productos base con información general
  - `ProductVariant`: Variantes de productos (color, tamaño, etc.)
  - `ProductImage`: Imágenes de productos (sistema legacy)
  - `ProductosMedia`: Sistema mejorado de imágenes de productos
  - `ItemStock`: Control de stock por producto y variante
- **`views.py`**: Vistas para catálogo, búsqueda, productos destacados y ofertas
- **`urls.py`**: Rutas del catálogo (home, productos, categorías, ofertas)
- **`admin.py`**: Configuración del panel de administración para productos
- **`management/commands/`**: Comandos personalizados para poblar datos

### **cart/** (Carrito de Compras)
- **`models.py`**: Modelos del carrito basado en sesiones
  - `Cart`: Carrito asociado a una sesión
  - `CartItem`: Items individuales en el carrito
- **`views.py`**: Lógica del carrito (agregar, remover, actualizar, aplicar cupones)
- **`urls.py`**: Rutas del carrito y operaciones AJAX

### **orders/** (Gestión de Órdenes)
- **`models.py`**: Modelos de órdenes y items
  - `Order`: Órdenes con información del cliente y envío
  - `OrderItem`: Items individuales de cada orden
- **`views.py`**: Procesamiento de checkout y visualización de órdenes
- **`forms.py`**: Formularios para datos de checkout
- **`urls.py`**: Rutas de órdenes y checkout
- **`admin.py`**: Configuración del admin para órdenes

### **warehouse/** (Control de Inventario)
- **`models.py`**: Modelos de inventario y despachos
  - `InventoryMovement`: Registro de movimientos de stock
  - `Shipment`: Registro de despachos
- **`views.py`**: Gestión de órdenes para despacho y control de inventario
- **`urls.py`**: Rutas del área de almacén
- **`admin.py`**: Configuración del admin para inventario

### **promotions/** (Sistema de Cupones)
- **`models.py`**: Modelo de cupones de descuento
  - `Coupon`: Cupones con diferentes tipos de descuento
- **`admin.py`**: Configuración del admin para cupones
- **`management/commands/`**: Comandos para crear y gestionar cupones

### **templates/** (Plantillas HTML)
- **`base.html`**: Plantilla base con navegación y estructura común
- **`catalog/`**: Plantillas del catálogo (home, productos, categorías, ofertas)
- **`cart/`**: Plantillas del carrito de compras
- **`orders/`**: Plantillas de checkout y detalle de órdenes
- **`warehouse/`**: Plantillas del área de almacén

### **static/** (Archivos Estáticos)
- **`css/`**: Hojas de estilo CSS
  - `base.css`: Estilos principales y navegación
  - `cart.css`: Estilos específicos del carrito
  - `checkout.css`: Estilos del proceso de checkout
  - `warehouse.css`: Estilos del área de almacén
  - `responsive.css`: Estilos para dispositivos móviles
- **`js/`**: Archivos JavaScript
  - `base.js`: Funcionalidad común (carrito, navegación)
  - `cart.js`: Funcionalidad específica del carrito
  - `warehouse.js`: Funcionalidad del área de almacén
- **`images/`**: Imágenes estáticas (logos, iconos)

### **media/** (Archivos Subidos)
- **`products/`**: Imágenes de productos subidas por usuarios
- **`categories/`**: Imágenes de categorías

### **entornovirtual/** (Entorno Virtual)
- **`Scripts/`**: Scripts de activación del entorno virtual
- **`Lib/`**: Librerías de Python instaladas
- **`pyvenv.cfg`**: Configuración del entorno virtual

## Decisiones Técnicas

### 1. **Arquitectura de Aplicaciones**
- **Separación por funcionalidad**: Cada aplicación maneja una responsabilidad específica
- **Modularidad**: Fácil mantenimiento y escalabilidad
- **Reutilización**: Componentes independientes y reutilizables

### 2. **Base de Datos PostgreSQL**
- **Robustez**: Mejor rendimiento para consultas complejas
- **Transacciones ACID**: Consistencia de datos garantizada
- **Escalabilidad**: Soporte para grandes volúmenes de datos
- **Soporte JSON**: Flexibilidad para datos no estructurados

### 3. **Sistema de Carrito Basado en Sesiones**
- **Sin autenticación**: Funciona para usuarios anónimos
- **Persistencia**: Carrito se mantiene entre páginas
- **Flexibilidad**: Fácil conversión a sistema con usuarios registrados

### 4. **Gestión de Inventario con Auditoría**
- **Trazabilidad completa**: Todos los movimientos se registran
- **Tipos de movimiento**: Entrada, salida y ajustes
- **Stock reservado**: Control de stock para carritos activos

### 5. **Sistema de Variantes de Productos**
- **Flexibilidad**: Productos con múltiples opciones
- **Stock independiente**: Cada variante tiene su propio stock
- **Precios diferenciados**: Modificadores de precio por variante

### 6. **Sistema de Cupones Flexible**
- **Tipos de descuento**: Porcentaje y monto fijo
- **Validaciones**: Fechas, límites de uso, montos mínimos
- **Control de uso**: Seguimiento de cupones utilizados

### 7. **Gestión de Imágenes Dual**
- **ProductImage**: Sistema legacy mantenido para compatibilidad
- **ProductosMedia**: Sistema mejorado con metadatos
- **Almacenamiento**: Archivos en sistema de archivos con referencias en BD

## Configuración de Desarrollo

### Base de Datos
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django2proyecto',
        'USER': 'postgres',
        'PASSWORD': '5102',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Archivos Estáticos y Media
```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Configuración Regional
```python
LANGUAGE_CODE = 'es-do'
TIME_ZONE = 'America/Santo_Domingo'
USE_I18N = True
USE_TZ = False
```

## Comandos de Gestión Personalizados

### Comandos Disponibles

```bash
# Poblar base de datos con productos y categorías
python manage.py populate_database

# Crear cupones de ejemplo
python manage.py create_coupons

# Crear imágenes de productos
python manage.py populate_product_media

# Probar flujo completo del e-commerce
python manage.py test_ecommerce_flow

# Migrar stock de productos
python manage.py migrate_stock

# Corregir fechas de cupones
python manage.py fix_coupon_dates
```

## Flujo de Funcionamiento

### 1. **Navegación y Catálogo**
- Usuario navega por categorías y productos
- Búsqueda de productos por nombre
- Visualización de productos destacados y ofertas

### 2. **Carrito de Compras**
- Agregar productos al carrito (con validación de stock)
- Actualizar cantidades
- Aplicar cupones de descuento
- Remover productos

### 3. **Checkout**
- Formulario de datos de envío
- Aplicación de cupones
- Creación de orden
- Confirmación de compra

### 4. **Gestión de Almacén**
- Visualización de órdenes pendientes
- Confirmación de órdenes
- Marcado como listo para despacho
- Despacho con registro de inventario

## Seguridad

### Medidas Implementadas
- **CSRF Protection**: Habilitado por defecto
- **Session Security**: Configuración segura de sesiones
- **SQL Injection**: Protegido por el ORM de Django
- **XSS Protection**: Configurado en middleware
- **Validación de datos**: Formularios con validación completa

### Variables Sensibles
- **SECRET_KEY**: Debe ser única y secreta
- **Database Credentials**: Usar variables de entorno
- **Debug Mode**: Deshabilitar en producción

## Despliegue en Producción

### Configuración de Producción
1. **Cambiar DEBUG a False**
2. **Configurar SECRET_KEY segura**
3. **Configurar ALLOWED_HOSTS**
4. **Configurar base de datos de producción**
5. **Configurar archivos estáticos**

### Comandos de Despliegue
```bash
# Recolectar archivos estáticos
python manage.py collectstatic

# Ejecutar con Gunicorn
gunicorn ferreteria_ecommerce.wsgi:application

# O con el servidor de desarrollo
python manage.py runserver 0.0.0.0:8000
```

## Recursos Adicionales

- [Documentación de Django](https://docs.djangoproject.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Django Admin Documentation](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)

---

**Desarrollado usando Django 5.2.5**
