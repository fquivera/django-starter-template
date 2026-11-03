# Django Fullstack Starter Template

[![Django 5.2](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![HTMX 2.0](https://img.shields.io/badge/HTMX-2.0-336699?logo=htmx&logoColor=white)](https://htmx.org/)
[![DaisyUI 4](https://img.shields.io/badge/DaisyUI-4-5A0EF8?logo=daisyui&logoColor=white)](https://daisyui.com/)
[![Alpine.js 3](https://img.shields.io/badge/Alpine.js-3-8BC0D0?logo=alpinedotjs&logoColor=white)](https://alpinejs.dev/)
[![uv](https://img.shields.io/badge/uv-Package%20Manager-DE5FE9)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/badge/Code%20Style-Ruff-black)](https://github.com/astral-sh/ruff)

Plantilla base y esqueleto de producción para proyectos **Django Fullstack** modernos utilizando la arquitectura **Server-Driven Web Application**: Django como fuente única de la verdad, HTMX para sincronización de fragmentos HTML reactivos sin SPA, DaisyUI + Tailwind CSS para componentes de diseño temáticos, y Alpine.js para estado transitorio en cliente.

Incluye configuración completa para desarrollo asistido por **Agentes de Inteligencia Artificial** con 24 SKILLS arquitectónicas pre-instaladas.

---

## 🎯 Características Principales

- **Gestión Ultrarrápida de Dependencias**: Administrado con [`uv`](https://github.com/astral-sh/uv) para resolución e instalación de paquetes en segundos.
- **Configuración Dividida por Entornos**: `config/settings/` separado en `base.py`, `development.py`, `production.py` y `test.py` con `django-environ`.
- **Modelo de Usuario Personalizado**: `apps.users.User` pre-configurado desde el día cero para evitar bloqueos de migraciones.
- **DaisyUI 4 + Tailwind CSS 3**: Sistema de diseño con temas intercambiables en tiempo real (`corporate`, `emerald`, `winter`, `light`, `dark`, etc.) persistidos en `localStorage`.
- **HTMX 2 + Alpine.js 3 Pre-cableados**:
  - Inyección global de token CSRF en todas las peticiones `hx-*`.
  - Shell de Modal Dinámico servido bajo demanda vía HTMX y animado con Alpine.
  - Contenedor de Alertas Toast Out-of-Band (`hx-swap-oob`) con auto-cierre.
- **Listo para Producción**: WhiteNoise con compresión Brotli y cache-busting, Gunicorn, PostgreSQL vía `psycopg[binary]`.
- **Quality Gates y Testing**: Configurado con `pytest`, `pytest-django` (settings en memoria ultra veloces) y `ruff` para linting y formateo.
- **AI Agent Ready**: Directorio `.agents/skills/` con 24 guías de ingeniería y `AGENTES.md` para dirigir LLMs con precisión.

---

## 📁 Estructura del Proyecto

```text
django-starter-template/
├── .agents/                      # Catálogo de 24 Skills de desarrollo para Agentes IA
│   └── skills/
├── apps/                         # Aplicaciones de dominio del proyecto
│   ├── core/                     # App principal: Landing, demos HTMX, healthcheck
│   │   ├── apps.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── tests.py
│   └── users/                    # Custom User Model & Admin
│       ├── apps.py
│       ├── admin.py
│       ├── models.py
│       ├── urls.py
│       └── tests.py
├── common/                       # Utilidades transversales y context processors
├── config/                       # Paquete de configuración del proyecto (NO una app)
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── development.py
│       ├── production.py
│       └── test.py
├── static/
│   ├── css/
│   │   ├── input.css             # Tailwind CSS + DaisyUI source
│   │   └── dist/output.css       # CSS compilado y minificado
│   └── js/
│       ├── htmx.min.js           # HTMX vendor script
│       └── alpine.min.js         # Alpine.js vendor script
├── templates/
│   ├── base.html                 # Layout maestro con CSRF, Navbar, Modales y Toasts
│   ├── components/               # Componentes reutilizables
│   │   ├── _navbar.html          # Barra de navegación con selector de tema DaisyUI
│   │   ├── _modal_shell.html     # Modal reactivo controlado por Alpine
│   │   └── _toast_container.html # Contenedor de notificaciones flotantes
│   └── pages/
│       ├── home.html             # Página principal con demostraciones en vivo
│       └── partials/
│           ├── _counter_box.html # Fragmento reactivo HTMX con OOB toast
│           └── _modal_demo.html  # Cuerpo de modal cargado dinámicamente
├── AGENTES.md                    # Manual y directivas para Agentes de IA
├── manage.py
├── package.json                  # Scripts y dependencias de Tailwind CSS + DaisyUI
├── pyproject.toml                # Dependencias Python y configuración de herramientas
├── tailwind.config.js            # Configuración de Tailwind y temas DaisyUI
└── README.md
```

---

## 🚀 Inicio Rápido (Quickstart)

### Prerrequisitos
- **Python 3.11+**
- [**uv**](https://docs.astral.sh/uv/getting-started/installation/) instalado (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Node.js 18+** y **npm**

### Paso 1: Clonar / Copiar la plantilla para un nuevo proyecto
```bash
# Copiar esta plantilla a una nueva carpeta de proyecto
cp -r django-starter-template mi-nuevo-proyecto
cd mi-nuevo-proyecto
```

### Paso 2: Crear el entorno y variables de configuración
```bash
cp .env.example .env
```
*(Edita `.env` si deseas cambiar el secreto o conectar a PostgreSQL)*

### Paso 3: Instalar dependencias con `uv`
```bash
# Crea el virtualenv e instala dependencias sincronizadas
uv sync
```

### Paso 4: Instalar y compilar el diseño (DaisyUI + Tailwind)
```bash
npm install
npm run build:css
```

### Paso 5: Aplicar migraciones iniciales y crear superusuario
```bash
uv run python manage.py migrate
uv run python manage.py createsuperuser
```

### Paso 6: Iniciar los servidores de desarrollo
Abre dos terminales:

**Terminal 1 (Servidor Django):**
```bash
uv run python manage.py runserver
```

**Terminal 2 (Compilación CSS en vivo):**
```bash
npm run watch:css
```

Accede a:
- 🌐 **Aplicación Web**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- ⚙️ **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- 🩺 **Health Check API**: [http://127.0.0.1:8000/health/](http://127.0.0.1:8000/health/)

---

## 🛠️ Comandos de Desarrollo Frecuentes

| Tarea | Comando |
|---|---|
| **Ejecutar Tests** | `uv run pytest` |
| **Auditar Calidad y Tipado** | `uv run ruff check .` |
| **Formatear Código** | `uv run ruff format .` |
| **Verificar Sistema Django** | `uv run python manage.py check` |
| **Verificar Migraciones** | `uv run python manage.py makemigrations --check --dry-run` |
| **Compilar CSS para Producción** | `npm run build:css` |

---

## 🧠 Desarrollo Asistido por Agentes de IA

Si estás utilizando **Google Antigravity, Claude, Cursor, Copilot o agentes CLI**:
1. Consulta [`AGENTES.md`](./AGENTES.md) para conocer las reglas de juego y compuertas de calidad.
2. La carpeta [`.agents/skills/`](./.agents/skills/) contiene 24 especificaciones detalladas para cada aspecto de Django (arquitectura en capas, modularización con `django-modular-apps`, protección contra IDOR en `django-security-permissions`, migraciones seguras en `django-migrations-patterns` y componentes en `django-htmx-components`).

---

## 🚢 Despliegue en Producción

Para desplegar en servidores Linux, contenedores Docker o plataformas PaaS:

1. **Variables de Entorno**: Establece `DJANGO_SETTINGS_MODULE=config.settings.production`, `DJANGO_DEBUG=False`, `DJANGO_SECRET_KEY` y `DATABASE_URL=postgresql://...`.
2. **Compilar Assets**: Ejecuta `npm run build:css` y luego `uv run python manage.py collectstatic --noinput`.
3. **Servidor WSGI**: Inicia el proceso con Gunicorn:
   ```bash
   uv run gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
   ```
