# Guía de Trabajo para Agentes de Inteligencia Artificial (`AGENTES.md`)

Este documento establece las **reglas de interacción, principios arquitectónicos y estándares de ingeniería** que cualquier Agente de IA (Antigravity, Claude, Cursor, Copilot o agentes CLI) debe seguir al desarrollar, refactorizar o extender este proyecto.

---

## 1. Filosofía del Stack Tecnológico

El proyecto implementa una arquitectura **Server-Driven Web Application**:

- **Django 5.2 LTS (Backend)**: Fuente única de la verdad (*Source of Truth*). Lógica de negocio, validaciones, permisos y persistencia residen en el servidor. Política LTS: mantener `django>=5.2.0,<5.3.0` (3 años de estabilidad y parches de seguridad en producción) sin actualizar a versiones intermedias no-LTS (`6.0`/`6.1`), hasta que se libere **Django 6.2 LTS**.
- **HTMX + `django-htmx` (Sincronización)**: Toda comunicación UI cliente-servidor intercambia fragmentos HTML (`_partial.html`). Las vistas detectan HTMX mediante `request.htmx` y **nunca** retornan JSON para la UI interna.
- **Tailwind CSS 4 + DaisyUI 5 (Diseño)**: Configuración *CSS-first* en `static/css/input.css` (`@import "tailwindcss";` + `@plugin "daisyui";`), compilado con `npm run build:css`. Uso estricto de tokens semánticos (`bg-base-100`, `text-base-content`, `btn-primary`, `alert-soft`, `menu-active`) e iconos SVG inline (Heroicons). Prohibido hardcodear colores hexadecimales o escalas `text-gray-*`.
- **Alpine.js 3 (Estado del Cliente)**: Gestiona exclusivamente estado visual transitorio del DOM que no persiste en servidor (modales, dropdowns, tabs, `ESC`, focus). Prohibido manipular el DOM con JS Vanilla o llamar `fetch()` desde Alpine.
- **Huey + Redis (Asíncrono Opcional)**: Cuando un proyecto requiera tareas en segundo plano o crons, utilizar **Huey** sobre Celery por su simplicidad, configuración mínima y bajo consumo de recursos.

---

## 2. Arquitectura de Skills en 2 Capas (`.agents/`)

Para minimizar el consumo de tokens de entrada por turno sin perder profundidad técnica, el repositorio usa **6 skills activas** auto-descubiertas y **6 skills on-demand** (0 tokens por defecto hasta que se lean explícitamente).

### Capa Activa (`.agents/skills/` — 6 Skills)

| Dimensión | Skill Canónica | Cuándo consultarla |
|---|---|---|
| **Arquitectura y Config** | `django-architecture` | Capas (`models`/`services`/`selectors`/`views`), paquetes modulares (`models/`, `views/`), settings y anti-hardcoding con `django-environ`. |
| **Modelos y Migraciones** | `django-models-migrations` | Diseño de modelos, `TextChoices`, QuerySets custom sin N+1, constraints y migraciones PostgreSQL *zero-downtime*. |
| **Vistas, Forms y Seguridad** | `django-views-forms-security` | Vistas delgadas, `ModelForm`/formsets, HTMX (`request.htmx`, `@vary_on_headers`, **HTTP 200** en errores), RBAC/IDOR (`visible_to`) e i18n base. |
| **Testing y Calidad** | `django-testing-quality` | Ciclo TDD con `pytest-django`, tests HTMX/IDOR/Huey y ejecución del Quality Gate (`uv`, `ruff`, `pytest`). |
| **Control de Versiones** | `git-workflow` | Flujo GitFlow (`main`, `develop`, `feat/*`, `release/*`, `hotfix/*`) y Conventional Commits. |
| **Frontend Hipermedia/UI** | `django-hypermedia-ui` | **Solo** al editar templates HTML, parciales `_*.html`, HTMX/Alpine, Tailwind 4 + DaisyUI 5 o SVGs inline (guías detalladas en `references/` y `components/`). |

### Capa Especializada On-Demand (`.agents/skills-ondemand/` — 0 Tokens por Defecto)

Leer explícitamente solo cuando la tarea involucre alguno de estos temas:

- `.agents/skills-ondemand/huey-patterns/SKILL.md`: Tareas asíncronas, reintentos, locks y crons con Huey + Redis (en lugar de Celery).
- `.agents/skills-ondemand/django-infrastructure/SKILL.md`: Docker multi-stage non-root, Gunicorn, Compose, WhiteNoise, build CSS y cabeceras CSP.
- `.agents/skills-ondemand/django-admin-expert/SKILL.md`: Optimización de Django Admin (cero N+1, `autocomplete_fields`, acciones en lote atómicas).
- `.agents/skills-ondemand/github-actions/SKILL.md`: Workflows de CI/CD, validación de CSS drift, política de ramas y releases.
- `.agents/skills-ondemand/i18n/SKILL.md`: Extracción y compilación de catálogos `.po`/`.mo` (`makemessages`/`compilemessages`) y formato localizado.
- `.agents/skills-ondemand/systematic-debugging/SKILL.md`: Metodología de depuración en 4 fases (*Root Cause First*).

---

## 3. Reglas Arquitectónicas Inquebrantables

1. **Límites de Capa (Dónde va el código)**:
   - **Modelos**: Invariantes de fila única y cálculos derivados (`order.can_cancel()`). Prohibido enviar correos, hacer HTTP o encolar tareas Huey desde modelos.
   - **Servicios (`services.py` / `services/`)**: Orquestación entre múltiples agregados, `@transaction.atomic`, I/O externo y `transaction.on_commit()` para tareas Huey.
   - **Selectores (`selectors.py` / `selectors/`)**: Consultas de solo lectura reutilizables con `select_related` / `prefetch_related` y scope explícito de usuario.
   - **Vistas (`views.py` / `views/`)**: Traducción HTTP únicamente (autenticar, autorizar, validar `Form`, llamar 1 servicio/selector, renderizar).
2. **Modularización Progresiva**:
   - Apps pequeñas (`< 300–400` líneas): mantener archivos planos (`models.py`, `views.py`, etc.).
   - Apps complejas (`> 400–500` líneas o múltiples agregados): dividir en paquetes (`models/`, `views/`, etc.) re-exportando siempre con importaciones explícitas y `__all__` en `__init__.py`.
3. **Seguridad en Endpoints Parciales (Anti-IDOR)**:
   - Toda URL parcial HTMX es públicamente inspeccionable y debe aplicar idéntica autenticación, RBAC y scoping que una vista completa:
     ```python
     # Correcto:
     obj = get_object_or_404(Project.objects.visible_to(request.user), pk=pk)
     ```
4. **Contrato HTMX para Formularios y Caché**:
   - Si una vista cambia su respuesta según `request.htmx`, decorar con `@vary_on_headers("HX-Request")`.
   - Si un formulario enviado vía HTMX falla validación, **re-renderizar el parcial del formulario con HTTP 200** para que HTMX realice el swap (HTMX ignora respuestas 4xx por defecto).
5. **Herramientas Estándar**:
   - Python: **`uv`** (`uv run ...`).
   - CSS / UI: **`npm`** con **Tailwind CSS 4** y **DaisyUI 5** (`npm run build:css`).
   - Linter & Formatter: **`ruff`** (`ruff check` + `ruff format --check`).
   - Test Runner: **`pytest`** (`pytest-django`).

---

## 4. Compuerta de Calidad (Quality Gate)

Antes de dar por finalizada cualquier tarea, el agente **DEBE** ejecutar y aprobar todos estos comandos:

```bash
# 1. Integridad del proyecto Django y migraciones limpias
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run

# 2. Suite de tests automatizados
uv run pytest

# 3. Linting y formato
uv run ruff check .
uv run ruff format --check .
```

Si la tarea modificó plantillas HTML o estilos CSS, compilar y validar también los assets:

```bash
npm run build:css
```

---

## 5. Flujo GitFlow y Conventional Commits

- **Ramas**:
  - Nuevas funcionalidades y correcciones nacen desde `develop` (`feat/<slug>`, `fix/<slug>`, `refactor/<slug>`, `docs/<slug>`) y se integran vía PR con **Squash Merge** hacia `develop`.
  - `release/<version>` y `hotfix/<version>` nacen desde `main`, se integran a `main` con **Merge Commit (`--no-ff`)**, se etiquetan (`vX.Y.Z`) y se retro-fusionan hacia `develop`.
- **Commits y títulos de PR**: formato obligatorio `<type>(<scope>)!: <descripción>` en imperativo minúscula sin punto final (`feat(ui): ...`, `fix(core): ...`, `refactor(skills): ...`, `docs: ...`).

---

## 6. Crear una Nueva App de Dominio

1. Crear el directorio y generar la app dentro de `apps/`:
   ```bash
   mkdir -p apps/<nombre_app>
   uv run python manage.py startapp <nombre_app> apps/<nombre_app>
   ```
2. Actualizar `name = "apps.<nombre_app>"` en `apps/<nombre_app>/apps.py`.
3. Registrar `"apps.<nombre_app>.apps.<Nombre>Config"` en `LOCAL_APPS` dentro de `config/settings/base.py`.
4. Incluir sus rutas con namespace semántico en `config/urls.py`.
5. Añadir tests con `@pytest.mark.django_db` en `apps/<nombre_app>/tests.py` (o `tests/`).
