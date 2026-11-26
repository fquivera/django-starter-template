# Reusable Django + HTMX + Alpine + DaisyUI 5 Component Recipes

All endpoints below enforce authentication and row-level scoping (`visible_to(request.user)`), use `request.htmx`, return HTTP 200 on validation errors, and use DaisyUI 5 semantic tokens.

## 1. Dynamic Server-Rendered Modal

Modal shell lives once in `templates/components/_modal_shell.html` (included in `base.html`).

### Trigger Button

```html
<button
    type="button"
    hx-get="{% url 'orders:note-create-modal' order.pk %}"
    hx-target="#modal-content"
    hx-swap="innerHTML"
    x-on:click="$dispatch('open-modal')"
    class="btn btn-primary btn-sm"
>
    Add Note
</button>
```

### Django View & Modal Partial

```python
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render


@login_required
def note_create_modal(request, pk):
    order = get_object_or_404(Order.objects.visible_to(request.user), pk=pk)
    if request.method == "POST":
        form = OrderNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.order = order
            note.save()
            response = HttpResponse("")
            response["HX-Trigger"] = '{"close-modal": true, "refresh-notes": true}'
            return response
    else:
        form = OrderNoteForm()

    return render(
        request,
        "orders/partials/_note_modal_body.html",
        {"form": form, "order": order},
    )
```

```html
<!-- templates/orders/partials/_note_modal_body.html -->
<div class="flex items-center justify-between pb-3 border-b border-base-300">
    <h3 class="text-lg font-bold">Add Note</h3>
    <button
        type="button"
        x-on:click="$dispatch('close-modal')"
        class="btn btn-sm btn-circle btn-ghost"
        aria-label="Close modal"
    >
        &times;
    </button>
</div>

<form
    hx-post="{% url 'orders:note-create-modal' order.pk %}"
    hx-target="#modal-content"
    hx-swap="innerHTML"
    hx-disabled-elt="find button[type='submit']"
    class="mt-4 space-y-4"
>
    {{ form.as_p }}
    <div class="modal-action">
        <button type="button" x-on:click="$dispatch('close-modal')" class="btn btn-ghost btn-sm">
            Cancel
        </button>
        <button type="submit" class="btn btn-primary btn-sm">Save</button>
    </div>
</form>
```

## 2. Active Search with Debounce

```html
<div class="relative mb-4">
    <input
        type="search"
        name="q"
        value="{{ request.GET.q|default:'' }}"
        placeholder="Search..."
        hx-get="{% url 'orders:list' %}"
        hx-trigger="input changed delay:300ms, search"
        hx-target="#orders-table-body"
        hx-indicator="#search-spinner"
        class="input input-bordered w-full pr-10"
    />
    <span id="search-spinner" class="htmx-indicator loading loading-spinner loading-sm absolute right-3 top-3 text-primary"></span>
</div>

<table class="table">
    <thead>...</thead>
    <tbody id="orders-table-body">
        {% include "orders/partials/_order_rows.html" %}
    </tbody>
</table>
```

## 3. Out-of-Band (OOB) Updates & Toast Notifications

```html
<!-- 1. Main target swapped normally -->
<tr id="item-row-{{ item.pk }}">
    <td>{{ item.name }}</td>
    <td>{{ item.amount }}</td>
</tr>

<!-- 2. OOB badge refresh -->
<div id="order-total-badge" hx-swap-oob="true" class="badge badge-success">
    Total: {{ order.total }}
</div>

<!-- 3. OOB DaisyUI toast appended to #toast-container -->
<div id="toast-container" hx-swap-oob="beforeend">
    <div
        x-data="{ show: true }"
        x-show="show"
        x-init="setTimeout(() => show = false, 3500)"
        class="alert alert-success shadow-lg max-w-sm"
    >
        <span class="text-sm font-medium">Saved successfully.</span>
    </div>
</div>
```

## 4. Inline Row Editing

### Display Row (`_item_row.html`)

```html
<tr id="item-row-{{ item.pk }}">
    <td>{{ item.description }}</td>
    <td>{{ item.amount }}</td>
    <td class="text-right">
        <button
            type="button"
            hx-get="{% url 'orders:item-edit-row' item.pk %}"
            hx-target="#item-row-{{ item.pk }}"
            hx-swap="outerHTML"
            class="btn btn-ghost btn-xs"
        >
            Edit
        </button>
    </td>
</tr>
```

### Edit Row Form (`_item_edit_row.html`)

```html
<tr id="item-row-{{ item.pk }}" class="bg-base-200/70">
    <td colspan="3">
        <form
            hx-post="{% url 'orders:item-edit-row' item.pk %}"
            hx-target="#item-row-{{ item.pk }}"
            hx-swap="outerHTML"
            class="flex flex-wrap items-center gap-2"
        >
            <input type="text" name="description" value="{{ form.description.value|default:'' }}" class="input input-bordered input-sm flex-1" />
            <input type="number" step="0.01" name="amount" value="{{ form.amount.value|default:'' }}" class="input input-bordered input-sm w-28" />
            <button type="submit" class="btn btn-success btn-sm">Save</button>
            <button
                type="button"
                hx-get="{% url 'orders:item-display-row' item.pk %}"
                hx-target="#item-row-{{ item.pk }}"
                hx-swap="outerHTML"
                class="btn btn-ghost btn-sm"
            >
                Cancel
            </button>
        </form>
    </td>
</tr>
```

## 5. Infinite Scroll / Lazy Table Loading

```html
{% for item in page_obj %}
    {% include "orders/partials/_order_row.html" with item=item only %}
{% empty %}
    <tr>
        <td colspan="4" class="text-center py-6 text-base-content/60">No records found.</td>
    </tr>
{% endfor %}

{% if page_obj.has_next %}
<tr
    hx-get="{% url 'orders:list' %}?page={{ page_obj.next_page_number }}"
    hx-trigger="revealed"
    hx-swap="outerHTML"
>
    <td colspan="4" class="text-center py-4 text-base-content/60">
        <span class="loading loading-spinner loading-sm text-primary mr-2"></span>
        Loading more...
    </td>
</tr>
{% endif %}
```
