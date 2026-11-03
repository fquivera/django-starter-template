# Guía de Trabajo para Agentes de Inteligencia Artificial (AGENTES.md)

Este documento establece las **reglas de interacción, principios arquitectónicos y estándares de ingeniería** que cualquier Agente de IA (Antigravity, Claude, Cursor, Copilot o scripts autónomos) debe seguir estrictamente al desarrollar, refactorizar o extender este proyecto.

---

## 1. Filosofía del Stack Tecnológico

El proyecto está diseñado bajo el paradigma **Server-Driven Web Application**:
- **Django (Backend)**: Fuente única de la verdad (*Source of Truth*). La lógica de negocio, validaciones y persistencia residen exclusivamente en el servidor.
- **HTMX (Sincronización)**: Maneja toda la comunicación cliente-servidor mediante intercambio de fragmentos HTML (`_partial.html`). Prohibido crear endpoints que retornen JSON para la UI interna; las vistas HTMX devuelven HTML listo para renderizar.
- **DaisyUI + Tailwind CSS (Diseño)**: Sistema de diseño semántico basado en clases utilitarias y componentes temáticos (`btn-primary`, `card`, `alert`, `modal-box`).
- **Alpine.js (Estado del Cliente)**: Controla única y exclusivamente el estado visual y transitorio del DOM que no requiere persistencia en servidor (abrir/cerrar modales, dropdowns, tabs locales, focus traps, atajos de teclado como `ESC`). Prohibido escribir JavaScript Vanilla desordenado.

---

## 2. Catálogo de SKILLS Disponibles (`.agents/skills/`)

Este repositorio incluye **24 SKILLS estandarizadas** en el directorio `.agents/skills/`. Antes de realizar cualquier cambio significativo, el agente debe consultar la skill especializada correspondiente:

| Dimensión | Skill Canónica | Cuándo consultarla |
|---|---|---|
| **Arquitectura de Apps** | `django-patterns` / `django-modular-apps` | Al diseñar nuevas apps o cuando una app crece a subpaquetes (`models/`, `views/`, etc.). |
| **Modelos y Queries** | `django-models` | Reglas de QuerySets custom, límite modelo vs servicio y optimización de ORM. |
| **Seguridad & Permisos** | `django-security-permissions` | Para proteger endpoints HTMX contra IDOR, scoping multitenancy y RBAC. |
| **Componentes UI** | `django-htmx-components` | Al crear modales dinámicos, búsquedas en vivo (debounce), swaps Out-of-Band o edición en línea. |
| **HTMX & Alpine** | `htmx-patterns` / `htmx-alpine` | Convenciones de cabeceras (`HX-Request`), CSRF, swaps y límites entre HTMX y Alpine. |
| **Migraciones de BD** | `django-migrations-patterns` | Para data migrations con `RunPython`, cero downtime y creación de índices concurrentes. |
| **Django Admin** | `django-admin-expert` | Para registrar modelos sin consultas N+1, autocomplete y acciones en lote. |
| **Formularios & Templates** | `django-forms` / `django-templates` | Validación en servidor, re-renderizado de errores 200 y parciales limpios. |
| **Calidad y Testing** | `pytest-django-patterns` / `code-quality` | Para escribir tests con fixtures y verificar ruff/pyright. |
| **Infraestructura** | `django-infrastructure` / `configuration` | Settings divididos, Docker, variables de entorno y despliegue. |
| **Control de Versiones** | `gitflow` / `conventional-commits` | Convención de ramas y formato de mensajes de commit (`feat:`, `fix:`). |

---

## 3. Reglas Arquitectónicas Inquebrantables

1. **Límites de Capa (Dónde va el código)**:
   - **Modelos**: Lógica de fila única o invariantes del agregado (`order.can_cancel()`, cálculos derivados).
   - **Servicios (`services.py` o `services/`)**: Orquestación entre múltiples modelos, transacciones atómicas (`@transaction.atomic`), llamadas externas o envíos de correo.
   - **Selectores (`selectors.py` o `selectors/`)**: Consultas de solo lectura reutilizables con `select_related` y `prefetch_related`.
   - **Vistas**: Traducción HTTP. Toman `request`, invocan el servicio o selector, y seleccionan el template o partial. Cero lógica de negocio en vistas.
2. **Modularización Progresiva**:
   - Apps pequeñas (< 300-400 líneas): Mantener archivos planos (`models.py`, `views.py`, etc.).
   - Apps complejas (> 400-500 líneas o múltiples agregados): Convertir en paquetes (`models/`, `views/`, etc.) exportando siempre vía `__all__` en `__init__.py` según `django-modular-apps`.
3. **Seguridad en Endpoints Parciales**:
   - Prohibido asumir que una URL HTMX no será vista por el usuario.
   - Todo endpoint de detalle o mutación debe resolver objetos filtrando por el usuario/organización autenticada:
     ```python
     # Correcto:
     get_object_or_404(Invoice.objects.visible_to(request.user), pk=pk)
     ```
4. **Respeto a las Herramientas Estándar**:
   - Gestor de paquetes Python: **`uv`**. Ejecutar comandos con `uv run ...`.
   - Gestor de assets CSS: **`npm`** con Tailwind CSS y DaisyUI.
   - Linter y Formatter: **`ruff`**.
   - Test Runner: **`pytest`**.

---

## 4. Compuerta de Calidad (Quality Gate)

Cualquier Agente de IA que termine una tarea o feature en este proyecto **DEBE** ejecutar y pasar con éxito estos tres comandos antes de entregar su respuesta al usuario:

```bash
# 1. Verificación de consistencia del sistema Django
uv run python manage.py check

# 2. Verificación de migraciones limpias (sin cambios pendientes)
uv run python manage.py makemigrations --check --dry-run

# 3. Suite de tests automatizados
uv run pytest

# 4. Auditoría de formato y calidad de código
uv run ruff check .
```

---

## 5. Instrucciones para Iniciar una Nueva Aplicación

Cuando se solicite al agente crear una nueva app de dominio:
1. Crear la app dentro del directorio `apps/`:
   ```bash
   mkdir -p apps/<nombre_app>
   uv run python manage.py startapp <nombre_app> apps/<nombre_app>
   ```
2. Modificar `apps/<nombre_app>/apps.py` para que el `name` sea `apps.<nombre_app>`.
3. Registrar `apps.<nombre_app>.apps.<Nombre>Config` en `LOCAL_APPS` dentro de `config/settings/base.py`.
4. Incluir sus rutas en `config/urls.py` con namespace semántico.
5. Crear sus tests correspondientes en `apps/<nombre_app>/tests.py`.
