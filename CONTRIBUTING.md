# Guía de Contribución (`CONTRIBUTING.md`)

¡Gracias por tu interés en contribuir a **Django Fullstack Starter Template**!

Esta plantilla está diseñada para mantenerse limpia, genérica y lista para producción sobre **Django 5.2 LTS + HTMX 2 + Alpine.js 3 + Tailwind CSS 4 + DaisyUI 5**.

---

## 1. Preparar Entorno Local

```bash
git clone git@github.com:fquivera/django-starter-template.git
cd django-starter-template
cp .env.example .env
uv sync
npm install
npm run build:css
uv run python manage.py migrate
```

---

## 2. Flujo GitFlow y Conventional Commits

1. **Ramas de trabajo:**
   - Crea tu rama siempre desde `develop`:
     ```bash
     git switch develop && git pull --ff-only origin develop
     git switch -c feat/mi-mejora
     ```
   - Prefijos recomendados: `feat/*`, `fix/*`, `docs/*`, `refactor/*`, `test/*`, `ci/*`, `chore/*`.
   - Las ramas `release/*` y `hotfix/*` nacen desde `main` y se integran con merge commit (`--no-ff`) y retro-fusión hacia `develop`.

2. **Formato de Commits y Título de PR (Conventional Commits):**
   ```text
   <type>(<scope>)!: <descripción en imperativo minúscula sin punto final>
   ```
   - Tipos válidos: `feat`, `fix`, `perf`, `refactor`, `docs`, `test`, `build`, `ci`, `style`, `chore`, `revert`.
   - Ámbitos sugeridos: `core`, `users`, `ui`, `common`, `config`, `deps`, `ci`, `skills`, `docs`, `release`.

---

## 3. Quality Gate Obligatorio

Antes de abrir tu Pull Request hacia `develop`, asegúrate de que todo pasa localmente:

```bash
npm run build:css
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

---

## 4. Principios para Cambios y Skills de IA

- **Mantén el starter genérico:** no incluyas lógica o nomenclatura específica de un negocio particular.
- **Política LTS:** mantenemos **Django 5.2 LTS** (`>=5.2.0,<5.3.0`) hasta el lanzamiento de **Django 6.2 LTS**.
- **Asíncrono recomendado:** documentar e integrar **Huey + Redis** antes que Celery.
- Si utilizas asistentes de IA o editas `.agents/`, consulta [`AGENTES.md`](./AGENTES.md) y [`.agents/skills/README.md`](./.agents/skills/README.md).
