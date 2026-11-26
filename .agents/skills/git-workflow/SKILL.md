---
name: git-workflow
description: >
  GitFlow branching/merge rules and Conventional Commits format for commits, PR titles, and releases.
  Use when creating branches, writing commit messages, opening PRs, or cutting releases/hotfixes.
---

# GitFlow & Conventional Commits

## 1. Branch Model & Merge Strategy

| Branch | Branches from | PR base | Merge strategy |
|---|---|---|---|
| `feature/<slug>`, `feat/<slug>`, `fix/<slug>`, `chore/*`, `docs/*`, `refactor/*`, `test/*`, `perf/*`, `build/*`, `ci/*` | `develop` | `develop` | **Squash** (PR title = commit) |
| `release/<version>` | `main` | `main` (+ back-merge `develop`) | **Merge commit (`--no-ff`)** |
| `hotfix/<version>` | `main` | `main` (+ back-merge `develop`) | **Merge commit (`--no-ff`)** |

- `main` and `develop` are protected: no direct pushes, never rebase or force-push shared branches.
- Naming: lowercase kebab-case, ASCII only (e.g. `feat/42-user-profile`, `fix/modal-focus-trap`). Delete branch after merge.

## 2. Conventional Commits

Format: `<type>(<scope>)!: <description>`

- Imperative, lowercase, no trailing period, header <= 100 chars (aim <= 72). One logical change per commit.
- **Types**: `feat` (minor), `fix` / `perf` (patch), `refactor`, `docs`, `test`, `build`, `ci`, `style`, `chore`, `revert`.
- **Scopes** (use the Django app or project area): `core`, `users`, `ui`, `common`, `config`, `deps`, `ci`, `skills`, `docs`, `release` (omit scope for repo-wide changes).
- **Breaking changes**: use `!` after scope/type AND a `BREAKING CHANGE:` footer with migration notes.
- **PR titles** into `develop` MUST follow Conventional Commits (squash merge turns the PR title into the commit message).

Daily commands, release/hotfix flows, commit body/revert examples, and branch protection rules: `references/release-and-commit-examples.md`.

## Integration with Other Skills

- `django-testing-quality`: Run full Quality Gate before opening any PR.
- `.agents/skills-ondemand/github-actions/SKILL.md`: CI status checks and release workflow.
