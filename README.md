# 🛒 Tienda Online Deportiva — E-Commerce con Django

Plataforma web de comercio electrónico para la venta de artículos deportivos, desarrollada con Django. Incluye gestión completa de productos, sistema de roles y administración de inventario.

---

## 🎯 Descripción del proyecto

Aplicación web full stack que simula una tienda deportiva en línea. El sistema permite a los administradores gestionar el catálogo de productos y a los usuarios navegar y realizar compras. El foco estuvo en construir una arquitectura limpia, modular y escalable usando las convenciones de Django.

---

## ✨ Funcionalidades principales

- **CRUD completo de productos** — Crear, leer, actualizar y eliminar artículos deportivos desde el panel de administración
- **Módulo de tienda** — Listado y vista detallada de productos disponibles
- **Gestión de imágenes** — Subida y visualización de imágenes de productos (`media/productos/`)
- **Sistema de tareas** — Módulo de gestión de tareas internas (`tasks/`)
- **Arquitectura modular** — Código organizado en apps de Django para facilitar escalabilidad

---

## 📁 Estructura del proyecto

```
E-commerce/
│
├── CRUD/                    # App Django para operaciones CRUD de productos
├── tienda/                  # App principal de la tienda (vistas, modelos, URLs)
├── tasks/                   # App de gestión de tareas internas
├── media/
│   └── productos/           # Imágenes subidas de los productos
│
├── manage.py                # Punto de entrada de Django
├── .gitignore
└── README.md
```

---

## 🛠 Tecnologías utilizadas

| Categoría | Tecnología |
|---|---|
| Backend | Python 3.x · Django |
| Frontend | HTML5 · CSS3 · JavaScript |
| Base de datos | MySQL (MySQL Workbench) |
| ORM | Django ORM |
| Control de versiones | Git / GitHub |

---

## 🚀 ¿Cómo ejecutar el proyecto localmente?

### 1. Clona el repositorio
```bash
git clone https://github.com/Zigartpro/E-commerce.git
cd E-commerce
```

### 2. Crea un entorno virtual e instala dependencias
```bash
python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate
pip install django mysqlclient pillow
```

### 3. Configura la base de datos
Edita `tienda/settings.py` con tus credenciales de MySQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce_db',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 4. Aplica las migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crea un superusuario y lanza el servidor
```bash
python manage.py createsuperuser
python manage.py runserver
```

Accede en `http://127.0.0.1:8000` y al panel admin en `http://127.0.0.1:8000/admin`

---

## 📸 Módulos del sistema

| Módulo | Descripción |
|---|---|
| `/tienda/` | Catálogo público de productos |
| `/CRUD/` | Gestión interna de inventario |
| `/tasks/` | Panel de tareas administrativas |
| `/admin/` | Panel de Django para gestión completa |

---

## 📌 Aprendizajes clave

- Desarrollo web full stack con el patrón MTV de Django
- Diseño e integración de base de datos relacional con MySQL
- Manejo de archivos multimedia con Django (subida y servicio de imágenes)
- Organización de proyectos en múltiples apps Django
- Implementación de sistema de roles con el ORM de Django

---

## 👤 Autor

**Duvan Federico Sarmiento Lugo**  
Ingeniero de Sistemas en formación | Full Stack Developer & Data Analyst  
📧 lugosarmiento7@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/duvansarmiento) | [GitHub](https://github.com/Zigartpro)
