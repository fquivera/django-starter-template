# DaisyUI 5 Component Index & Heroicons Snippets

Load to pick candidate DaisyUI components before reading `../components/<name>.md`.

## DaisyUI 5 Components (`../components/`)

- **Actions**: `button`, `dropdown`, `fab`, `modal`, `swap`, `theme-controller`
- **Data display**: `accordion`, `avatar`, `badge`, `card`, `carousel`, `chat`, `collapse`, `countdown`, `diff`, `hover-3d`, `hover-gallery`, `kbd`, `list`, `stat`, `status`, `table`, `text-rotate`, `timeline`
- **Navigation**: `breadcrumbs`, `dock`, `link`, `megamenu`, `menu`, `navbar`, `pagination`, `steps`, `tab`
- **Feedback**: `alert`, `loading`, `progress`, `radial-progress`, `skeleton`, `toast`, `tooltip`
- **Data input**: `calendar`, `checkbox`, `fieldset`, `file-input`, `filter`, `input`, `label`, `otp`, `radio`, `range`, `rating`, `select`, `textarea`, `toggle`, `validator`
- **Layout**: `aura`, `divider`, `drawer`, `footer`, `hero`, `indicator`, `join`, `mask`, `stack`
- **Mockups**: `mockup-browser`, `mockup-code`, `mockup-phone`, `mockup-window`

Each guide lives at `../components/<name>.md`. Read more than one candidate when the choice is not obvious.

## Heroicons Minimal Snippets

```html
<!-- Outline 24x24 icon -->
<svg xmlns="http://www.w3.org/2000/svg" class="size-4 opacity-60" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
  <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
</svg>

<!-- Icon-only button (aria-label required) -->
<button type="button" class="btn btn-ghost btn-sm btn-square" aria-label="Delete row">
  <svg xmlns="http://www.w3.org/2000/svg" class="size-4 text-error" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
  </svg>
</button>
```
