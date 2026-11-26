## Descripción

<!-- Resume qué resuelve este PR y por qué es necesario. -->

## Tipo de Cambio

- [ ] `feat`: Nueva funcionalidad (apunta a `develop`)
- [ ] `fix`: Corrección de bug (apunta a `develop`)
- [ ] `refactor` / `chore` / `docs` / `ci`: Mantenimiento o documentación
- [ ] `release/*` / `hotfix/*`: Promoción o parche hacia `main` (`--no-ff`)

## Quality Gate Checklist

- [ ] `uv run python manage.py check` pasa sin advertencias
- [ ] `uv run python manage.py makemigrations --check --dry-run` sin cambios pendientes
- [ ] `uv run pytest` pasa con cobertura para los cambios introducidos
- [ ] `uv run ruff check .` y `uv run ruff format --check .` pasan sin errores
- [ ] Si se modificaron templates o estilos: `npm run build:css` ejecutado y `static/css/dist/output.css` actualizado
- [ ] El título del PR sigue **Conventional Commits** (`<type>(<scope>): <description>`)
