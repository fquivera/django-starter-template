# GitFlow Commands & Conventional Commit Examples

## Daily Feature Flow

```bash
# Start from an up-to-date develop
git switch develop
git pull --ff-only origin develop
git switch -c feat/user-profile

# Work in atomic commits
git add -p
git commit -m "feat(users): add profile edit view and form"

# Keep branch current without rewriting shared history
git fetch origin
git rebase origin/develop   # only while branch is personal / not shared

# Push and open PR into develop
git push -u origin feat/user-profile
gh pr create --base develop --fill
```

## Release Flow (`SemVer`)

```bash
# 1. Cut release branch from main (or merge develop -> release/x.y.z)
git switch main && git pull --ff-only origin main
git switch -c release/0.2.0
git merge --no-ff origin/develop

# 2. Bump version + CHANGELOG, commit, push, PR -> main
git push -u origin release/0.2.0
gh pr create --base main --title "chore(release): prepare v0.2.0"

# 3. After CI passes and PR merges into main, tag main and back-merge into develop
git switch main && git pull --ff-only origin main
git tag -a v0.2.0 -m "v0.2.0"
git push origin v0.2.0

git switch develop && git pull --ff-only origin develop
git merge --no-ff main
git push origin develop
```

## Hotfix Flow

```bash
git switch main && git pull --ff-only origin main
git switch -c hotfix/0.2.1

# Fix + regression test
git commit -m "fix(users): prevent duplicate email signup race"
git push -u origin hotfix/0.2.1
gh pr create --base main --title "fix(users): prevent duplicate email signup race"

# After merge into main: tag v0.2.1 and back-merge main -> develop
```

## Conventional Commit Examples

Good:

```text
feat(ui): upgrade to Tailwind CSS 4 and DaisyUI 5
fix(core): return HTTP 200 on invalid HTMX form submissions
perf(users): select_related organization on dashboard query
refactor(skills): consolidate into layered active and on-demand skills
docs: update README and AGENTES.md for Tailwind 4 stack
test(core): verify Vary header on HTMX partial endpoints
build(deps): upgrade django to 5.2.x
ci: validate PR titles against Conventional Commits
```

With body and footer:

```text
fix(ui): preserve modal state on HTMX validation error

Re-rendering the modal body with HTTP 422 prevented HTMX from swapping
the error markup. Return status 200 for invalid HTMX form submissions.

Closes: #42
```

Breaking change:

```text
feat(config)!: require DJANGO_SECRET_KEY in production settings

BREAKING CHANGE: production startup now raises ImproperlyConfigured when
DJANGO_SECRET_KEY is unset or uses the development placeholder.
```

Revert:

```text
revert: feat(ui): add infinite scroll to items table

This reverts commit 1a2b3c4d5e6f.

Reason: infinite scroll broke keyboard pagination focus order.
```

## Recommended GitHub Branch Protection (`main` & `develop`)

- Require pull requests (no direct pushes).
- Require status checks to pass before merging (`lint`, `django`, `test`).
- Require branches to be up to date before merging.
- Block force pushes and branch deletions.
- Allow squash merges into `develop` and merge commits for `release/*` / `hotfix/*` into `main`.
