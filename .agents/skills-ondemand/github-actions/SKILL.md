---
name: github-actions
description: >
  GitHub Actions CI/CD for Django + uv + PostgreSQL + Ruff + pytest + Tailwind 4 CSS drift check + GitFlow PR policy.
  Use when editing workflows, debugging CI checks, or configuring automated releases.
---

# GitHub Actions CI/CD

## 1. CI Workflow (`.github/workflows/ci.yml`)

Triggers: `pull_request` into `main` / `develop`, and `push` to `main` / `develop`.

### Recommended Jobs

| Job | Purpose |
|---|---|
| `lint` | `uv run ruff check .`, `uv run ruff format --check .`, `npm ci && npm run build:css` + `git diff --exit-code -- static/css/dist/output.css` |
| `django` | `uv run python manage.py check`, `uv run python manage.py makemigrations --check --dry-run`, `check --deploy` (with production settings) |
| `test` | `uv run pytest` against PostgreSQL service container (`postgres:16`) |
| `branch-policy` | Enforces GitFlow (`feat/*`/`fix/*`/maintenance → `develop`; `release/*`/`hotfix/*`/`develop` → `main`) |
| `commit-messages` | Validates PR title (`develop` squash merge) or non-merge commit subjects against Conventional Commits |

### Non-Negotiables

- Set `permissions: contents: read` at workflow level; elevate only per job when needed.
- Use `concurrency` with `cancel-in-progress: true` on feature branches.
- Set `timeout-minutes` on every job.
- Use `astral-sh/setup-uv` with `enable-cache: true` (never cache `~/.cache/pip`).
- Pin third-party actions to specific version tags or SHAs; never echo secrets.

### Deployment Check Example

```yaml
- name: Django production check
  env:
    DJANGO_SETTINGS_MODULE: config.settings.production
    DJANGO_ALLOWED_HOSTS: example.com
    DJANGO_SECRET_KEY: ci-only-placeholder-key
  run: uv run python manage.py check --deploy
```

### CSS Drift Check Example

```yaml
- name: Verify compiled Tailwind 4 + DaisyUI 5 CSS
  run: |
    npm ci
    npm run build:css
    git diff --exit-code -- static/css/dist/output.css
```

## 2. Release Workflow (`.github/workflows/release.yml`)

- Trigger on pushed tags matching `v*.*.*`.
- Re-run verification (`lint`, `django`, `test`) before publishing artifacts or creating the GitHub Release (`gh release create "$TAG" --generate-notes`).
- Mark tags containing `-` (e.g. `v0.2.0-rc.1`) as prereleases.

## 3. Local Reproduction Before Pushing

```bash
npm run build:css
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

## Integration with Other Skills

- `git-workflow`: Branch naming, merge strategy, and Conventional Commits rules.
- `django-testing-quality`: Local Quality Gate matching CI jobs.
- `.agents/skills-ondemand/django-infrastructure/SKILL.md`: Production Docker image and settings checks.
