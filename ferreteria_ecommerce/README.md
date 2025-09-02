# 🛠️ Ferretería E-commerce - Sistema de Gestión Completo

## 📋 Descripción del Proyecto

Sistema de e-commerce completo para ferretería desarrollado en Django 5.2.5, que incluye gestión de catálogo, carrito de compras, órdenes, inventario y promociones. El proyecto está diseñado para manejar productos con variantes, control de stock, cupones de descuento y gestión de envíos.

## 🚀 Características Principales

- **Catálogo de Productos**: Gestión completa de productos con categorías jerárquicas
- **Sistema de Variantes**: Productos con diferentes opciones (color, tamaño, etc.)
- **Carrito de Compras**: Basado en sesiones con persistencia en base de datos
- **Gestión de Órdenes**: Flujo completo desde checkout hasta entrega
- **Control de Inventario**: Movimientos de stock y gestión de bodega
- **Sistema de Promociones**: Cupones de descuento configurables
- **Panel de Administración**: Interfaz Django Admin personalizada
- **Responsive Design**: Interfaz adaptativa para diferentes dispositivos

## 🏗️ Arquitectura del Sistema

### Aplicaciones Django

1. **`catalog`**: Gestión de productos, categorías e imágenes
2. **`cart`**: Carrito de compras y gestión de sesiones
3. **`orders`**: Procesamiento de órdenes y checkout
4. **`warehouse`**: Control de inventario y envíos
5. **`promotions`**: Sistema de cupones y descuentos

### Modelos de Datos Principales

- **Product**: Productos base con información general
- **ProductVariant**: Variantes de productos (color, tamaño, etc.)
- **Category**: Categorías jerárquicas de productos
- **Cart/CartItem**: Carrito de compras por sesión
- **Order/OrderItem**: Órdenes y sus items
- **InventoryMovement**: Movimientos de inventario
- **Coupon**: Cupones de descuento

## 🛠️ Requisitos del Sistema

### Software Requerido

- **Python**: 3.8 o superior
- **PostgreSQL**: 12 o superior
- **pip**: Gestor de paquetes de Python
- **Git**: Control de versiones

### Dependencias de Python

```
Django==5.2.5
psycopg2-binary==2.9.10
requests==2.32.4
Pillow==10.4.0
python-decouple==3.8
gunicorn==21.2.0
whitenoise==6.6.0
```

## 📦 Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd ferreteria_ecommerce
```

### 2. Crear Entorno Virtual

```bash
# Windows
python -m venv entornovirtual
entornovirtual\Scripts\activate

# Linux/Mac
python3 -m venv entornovirtual
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

Crear archivo `.env` en la raíz del proyecto:

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

### 8. Cargar Datos Iniciales (Opcional)

```bash
python manage.py loaddata base.sql
```

### 9. Ejecutar el Servidor

```bash
python manage.py runserver
```

El proyecto estará disponible en: http://127.0.0.1:8000/

## 🔧 Configuración de Desarrollo

### Configuración de Base de Datos

El proyecto está configurado para usar PostgreSQL con los siguientes parámetros por defecto:

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

### Configuración de Archivos Estáticos

```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Configuración de Internacionalización

```python
LANGUAGE_CODE = 'es-do'
TIME_ZONE = 'America/Santo_Domingo'
USE_I18N = True
USE_TZ = False
```

## 🗂️ Estructura del Proyecto

```
ferreteria_ecommerce/
├── catalog/                 # Aplicación de catálogo
│   ├── models.py           # Modelos de productos y categorías
│   ├── views.py            # Vistas del catálogo
│   ├── urls.py             # URLs del catálogo
│   └── admin.py            # Configuración del admin
├── cart/                   # Aplicación del carrito
│   ├── models.py           # Modelos del carrito
│   ├── views.py            # Vistas del carrito
│   └── urls.py             # URLs del carrito
├── orders/                 # Aplicación de órdenes
│   ├── models.py           # Modelos de órdenes
│   ├── views.py            # Vistas de órdenes
│   ├── forms.py            # Formularios de checkout
│   └── urls.py             # URLs de órdenes
├── warehouse/              # Aplicación de bodega
│   ├── models.py           # Modelos de inventario
│   ├── views.py            # Vistas de bodega
│   └── urls.py             # URLs de bodega
├── promotions/             # Aplicación de promociones
│   ├── models.py           # Modelos de cupones
│   └── admin.py            # Configuración del admin
├── templates/              # Plantillas HTML
│   ├── base.html           # Plantilla base
│   ├── catalog/            # Plantillas del catálogo
│   ├── cart/               # Plantillas del carrito
│   ├── orders/             # Plantillas de órdenes
│   └── warehouse/          # Plantillas de bodega
├── static/                 # Archivos estáticos
│   ├── css/                # Hojas de estilo
│   ├── js/                 # JavaScript
│   └── images/             # Imágenes
├── media/                  # Archivos subidos por usuarios
├── ferreteria_ecommerce/   # Configuración del proyecto
│   ├── settings.py         # Configuración de Django
│   ├── urls.py             # URLs principales
│   └── wsgi.py             # Configuración WSGI
└── manage.py               # Script de gestión de Django
```

## 🎯 Decisiones Técnicas

### 1. Base de Datos

**PostgreSQL**: Elegido por su robustez, soporte para transacciones complejas y manejo eficiente de datos relacionales.

**Razones**:
- Mejor rendimiento para consultas complejas
- Soporte nativo para JSON
- Transacciones ACID
- Escalabilidad

### 2. Gestión de Imágenes

**Almacenamiento en Base de Datos**: Las imágenes se almacenan como datos binarios en la base de datos en lugar de archivos en el sistema de archivos.

**Ventajas**:
- Consistencia de datos
- Fácil backup y restauración
- No hay problemas de sincronización entre archivos y base de datos

**Desventajas**:
- Mayor tamaño de base de datos
- Posible impacto en rendimiento para imágenes grandes

### 3. Sistema de Carrito

**Basado en Sesiones**: El carrito se asocia con la sesión del usuario, permitiendo persistencia entre páginas.

**Implementación**:
- Cada sesión tiene un carrito asociado
- Los items del carrito se almacenan en la base de datos
- Soporte para productos con variantes

### 4. Gestión de Inventario

**Movimientos de Stock**: Sistema de auditoría completa que registra todos los movimientos de inventario.

**Tipos de Movimientos**:
- `in`: Entrada de stock
- `out`: Salida de stock
- `adjustment`: Ajuste manual de stock

### 5. Sistema de Variantes

**Productos con Opciones**: Los productos pueden tener múltiples variantes (color, tamaño, material, etc.).

**Implementación**:
- Modelo `ProductVariant` relacionado con `Product`
- Cada variante puede tener su propio precio y stock
- SKU único por variante

### 6. Cupones de Descuento

**Sistema Flexible**: Soporte para descuentos porcentuales y de monto fijo.

**Características**:
- Fechas de validez
- Límites de uso
- Montos mínimos de compra
- Descuentos máximos

## 🚀 Despliegue en Producción

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

## 🧪 Testing

### Ejecutar Tests

```bash
# Tests de todas las aplicaciones
python manage.py test

# Tests de una aplicación específica
python manage.py test catalog
python manage.py test cart
python manage.py test orders
```

## 📊 Comandos de Gestión Personalizados

El proyecto incluye comandos de gestión personalizados para tareas administrativas:

```bash
# Comandos disponibles
python manage.py help

# Comandos específicos del proyecto
python manage.py [nombre_del_comando]
```

## 🔒 Seguridad

### Consideraciones de Seguridad

- **CSRF Protection**: Habilitado por defecto
- **Session Security**: Configuración segura de sesiones
- **SQL Injection**: Protegido por el ORM de Django
- **XSS Protection**: Configurado en middleware

### Variables Sensibles

- **SECRET_KEY**: Debe ser única y secreta
- **Database Credentials**: Usar variables de entorno
- **Debug Mode**: Deshabilitar en producción

## 📈 Monitoreo y Logs

### Logs de Django

Los logs se configuran en `settings.py` y pueden incluir:
- Errores de aplicación
- Accesos a la base de datos
- Operaciones de seguridad

### Métricas Recomendadas

- Tiempo de respuesta de páginas
- Uso de base de datos
- Errores 4xx y 5xx
- Uso de memoria y CPU

## 🤝 Contribución

### Estándares de Código

- Seguir PEP 8 para Python
- Usar nombres descriptivos para variables y funciones
- Documentar funciones complejas
- Mantener consistencia en el estilo

### Flujo de Trabajo

1. Crear rama para nueva funcionalidad
2. Implementar cambios
3. Ejecutar tests
4. Crear pull request
5. Revisión de código

## 📞 Soporte

### Contacto

Para soporte técnico o preguntas sobre el proyecto:
- Crear un issue en el repositorio
- Documentar el problema con detalles
- Incluir logs y pasos para reproducir

### Recursos Adicionales

- [Documentación de Django](https://docs.djangoproject.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Django Admin Documentation](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)

## 📄 Licencia

Este proyecto está bajo la licencia [especificar licencia].

---

**Desarrollado con ❤️ usando Django 5.2.5**
