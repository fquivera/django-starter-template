---
name: django-hypermedia-ui
description: >
  Django templates/partials, HTMX + Alpine.js rules, Tailwind CSS 4 + DaisyUI 5 components/tokens, and inline SVG icons.
  Use only when editing HTML templates, HTMX partials, Alpine client state, or Tailwind/DaisyUI styling.
---

# Django Hypermedia UI (Templates + HTMX + Alpine.js + DaisyUI 5)

Server-driven UI rules: **Django is the single source of truth** (returns HTML fragments, never JSON for internal UI).

## 1. Division of Labor

| Need | Use | Never Use |
|---|---|---|
| Server roundtrip (forms, search, pagination, mutations) | HTMX (`hx-get`, `hx-post`, `hx-target`, `hx-swap`) | `fetch()` / JSON UI endpoints |
| Transient client-only UI (modal open/close, dropdowns, tabs, `ESC`, focus) | Alpine.js (`x-data`, `x-show`, `x-cloak`, `static/js/alpine.min.js`) | Vanilla JS DOM manipulation or storing server state in Alpine |
| Styling & components | Tailwind CSS 4 + DaisyUI 5 semantic classes | Hardcoded `#hex`, `bg-white`, `text-gray-*`, or custom CSS |
| Icons | Inline Heroicons SVGs (`heroicons.com`) | npm icon packs or icon template tags |

## 2. Template Layout & Conventions

```text
templates/
├── base.html                 # Root shell, CSRF hx-headers, navbar, modal shell, toast container
├── components/               # Shared UI blocks (_navbar.html, _modal_shell.html, _toast_container.html)
└── pages/
    ├── <page>.html           # Full pages extending base.html
    └── partials/_*.html      # Self-contained HTMX fragments (underscore prefix, no {% extends %})
```

- Isolate component context with `{% include "components/_card.html" with title=obj.title only %}`.
- Keep business logic out of templates (use model properties/selectors). Always use `{% url %}` (never hardcoded paths), `{% empty %}` in loops, and `{% translate %}` for user-facing text.

## 3. Django + HTMX Rules

- Detect HTMX via `request.htmx` (`django-htmx`) and decorate views whose response varies by HTMX with `@vary_on_headers("HX-Request")`.
- **CSRF**: configured globally on `<body>` via `hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'` (never cache HTML containing it).
- **Form errors**: re-render the form partial with **HTTP 200** so HTMX swaps it.
- **Feedback & UX**: always use `hx-indicator`, `hx-disabled-elt="this"` on submit buttons, and OOB toasts (`#toast-container`) / `HX-Trigger` instead of Django `messages`.
- **Response headers**: `HX-Trigger`, `HX-Redirect`, `HX-Retarget`/`HX-Reswap`, `HX-Refresh`.
- **Accessibility**: `x-cloak` on Alpine toggles, `aria-live="polite"` on dynamic containers, focus management on modals/swaps.

## 4. DaisyUI 5 + Tailwind CSS 4 & Inline SVG Icons

1. Look up candidate components in `references/component-index.md` and read `./components/<name>.md` before writing markup; obey exact component DOM structure and constraints.
2. Read `./usage/SKILL.md` for class-naming rules and `./colors/SKILL.md` for semantic color tokens (`bg-base-100`, `bg-base-200`, `text-base-content/70`, `btn-primary`, `alert-soft`). Never hardcode palette grays or hex colors.
3. Run `npm run build:css` after template or `static/css/input.css` edits.
4. **Heroicons inline SVGs**: add `aria-hidden="true"` on `<svg>` (and `aria-label="..."` on icon-only buttons/links); inherit `currentColor`; use `size-4` (buttons/tables), `size-5` (nav), `size-6`–`size-8` (empty states/modals); default to Outline 24x24 (`fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"`).

## 5. On-Demand References (Load Only What You Need)

| Topic | Reference File |
|---|---|
| Modals, active search, OOB toasts, inline row edit, infinite scroll (DaisyUI 5 + IDOR-safe) | `references/htmx-components.md` |
| DaisyUI 5 component index (68 components) & Heroicons snippets | `references/component-index.md` |
| DaisyUI 5 rules, colors, config, component docs | `./usage/SKILL.md`, `./colors/SKILL.md`, `./config/SKILL.md`, `./components/<name>.md` |
| `hx-get`/`hx-post`/`hx-target`/`hx-swap` details | `references/htmx-requests.md` |
| Alpine `x-data`/`x-model` state patterns | `references/alpine-state.md` |
| Coordinating HTMX + Alpine & confirm dialogs | `references/integration.md` |
| Loading spinners & error feedback | `references/feedback-patterns.md` |
| Focus management, ARIA, screen readers | `references/accessibility.md` |
| SSE / WebSocket extensions | `references/realtime.md` |

## Integration with Other Skills

- `django-views-forms-security`: Scoped QuerySets (`visible_to`), RBAC, and form validation.
- `django-testing-quality`: Testing HTMX partial rendering, `Vary` headers, and running `npm run build:css`.
