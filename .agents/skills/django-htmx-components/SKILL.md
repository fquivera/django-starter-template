---
name: django-htmx-components
description: Reusable UI component patterns combining Django templates, HTMX swaps, and Alpine.js client state. Use when building dynamic modals, active search/typeahead, out-of-band (OOB) updates, inline row editing, or infinite scroll.
---

# Django + HTMX + Alpine UI Component Patterns

Reusable, production-tested interaction patterns combining Django server rendering, HTMX HTML swaps, and Alpine.js client-side reactivity.

---

## 1. Core Component Division of Labor

To prevent conflicting state, DOM re-render glitches, and broken event listeners:

| Responsibility | Technology | Example |
|---|---|---|
| **Server State & HTML Rendering** | Django Templates + Views | Generates HTML partials, validates form input, persists data |
| **Server Synchronization** | HTMX (`hx-*`) | Requests fragments, handles swaps, triggers server events |
| **Client Transient State** | Alpine.js (`x-*`) | Open/closed modals, dropdowns, keyboard events, focus traps |

---

## 2. Dynamic Server-Rendered Modal

A dynamic modal loads its body on demand from Django, while Alpine controls open/close visibility, backdrop, and keyboard shortcuts (`ESC`).

### 2.1 The Modal Shell (in `base.html` or Layout)
Place the modal container outside main content wrappers:

```html
<!-- Modal Shell in base.html -->
<div
    x-data="{ open: false, url: '' }"
    x-show="open"
    x-on:open-modal.window="open = true; if ($event.detail.url) { url = $event.detail.url; }"
    x-on:close-modal.window="open = false; $refs.modalContent.innerHTML = ''"
    x-on:keydown.escape.window="open = false; $refs.modalContent.innerHTML = ''"
    x-cloak
    class="fixed inset-0 z-50 overflow-y-auto"
>
    <!-- Backdrop -->
    <div
        x-show="open"
        x-transition:enter="ease-out duration-300"
        x-transition:enter-start="opacity-0"
        x-transition:enter-end="opacity-100"
        x-transition:leave="ease-in duration-200"
        x-transition:leave-start="opacity-100"
        x-transition:leave-end="opacity-0"
        class="fixed inset-0 bg-black/50 transition-opacity"
        x-on:click="open = false; $refs.modalContent.innerHTML = ''"
    ></div>

    <!-- Modal Dialog Body -->
    <div class="flex min-h-full items-center justify-center p-4">
        <div
            x-show="open"
            x-transition:enter="ease-out duration-300"
            x-transition:enter-start="opacity-0 scale-95"
            x-transition:enter-end="opacity-100 scale-100"
            x-transition:leave="ease-in duration-200"
            x-transition:leave-start="opacity-100 scale-100"
            x-transition:leave-end="opacity-0 scale-95"
            x-ref="modalContent"
            id="modal-content"
            class="relative w-full max-w-lg rounded-lg bg-white p-6 shadow-xl"
            x-on:click.stop
        >
            <!-- Loaded via HTMX -->
        </div>
    </div>
</div>
```

### 2.2 Trigger Button
```html
<button
    type="button"
    hx-get="{% url 'billing:payment-create-modal' invoice.pk %}"
    hx-target="#modal-content"
    hx-swap="innerHTML"
    x-on:click="$dispatch('open-modal')"
    class="btn-primary"
>
    Record Payment
</button>
```

### 2.3 Django Modal Partial View & Template
```python
# apps/billing/views/payments.py
from django.shortcuts import render, get_object_or_404
from ..models import Invoice
from ..forms import PaymentForm


def payment_create_modal(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.invoice = invoice
            payment.save()
            # Return empty response with close event + trigger table refresh
            response = render(request, "billing/partials/_empty.html")
            response["HX-Trigger"] = '{"close-modal": true, "refresh-payments": true}'
            return response
    else:
        form = PaymentForm(initial={"amount": invoice.remaining_balance})

    return render(
        request,
        "billing/partials/_payment_modal_body.html",
        {"form": form, "invoice": invoice},
    )
```

```html
<!-- apps/billing/templates/billing/partials/_payment_modal_body.html -->
<div class="flex justify-between items-center mb-4">
    <h3 class="text-lg font-bold">Record Payment for Invoice #{{ invoice.number }}</h3>
    <button type="button" x-on:click="$dispatch('close-modal')" class="text-gray-400 hover:text-gray-600">
        &times;
    </button>
</div>

<form
    hx-post="{% url 'billing:payment-create-modal' invoice.pk %}"
    hx-target="#modal-content"
    hx-swap="innerHTML"
>
    {% csrf_token %}
    {{ form.as_p }}
    <div class="mt-4 flex justify-end gap-2">
        <button type="button" x-on:click="$dispatch('close-modal')" class="btn-secondary">Cancel</button>
        <button type="submit" class="btn-primary">Save Payment</button>
    </div>
</form>
```

---

## 3. Active Search with Debounce & Focus Preservation

For live filtering tables without full page reloads:

```html
<div class="relative mb-4">
    <input
        type="search"
        name="q"
        value="{{ request.GET.q|default:'' }}"
        placeholder="Search invoices by number or client..."
        hx-get="{% url 'billing:invoice-list-table' %}"
        hx-trigger="input changed delay:300ms, search"
        hx-target="#invoice-table-body"
        hx-indicator="#search-spinner"
        class="input-search w-full"
    />
    <div id="search-spinner" class="htmx-indicator absolute right-3 top-2.5">
        <svg class="animate-spin h-5 w-5 text-gray-500" viewBox="0 0 24 24">...</svg>
    </div>
</div>

<table class="min-w-full">
    <thead>...</thead>
    <tbody id="invoice-table-body">
        {% include "billing/partials/_invoice_table_rows.html" %}
    </tbody>
</table>
```

---

## 4. Out-of-Band (OOB) Updates & Toast Notifications

When a single action needs to update its target **plus** another area of the screen (e.g. Updating an item row and refreshing the total balance in the header):

### 4.1 Server Response Partial with `hx-swap-oob`
```html
<!-- Returned by POST /invoices/12/items/add/ -->

<!-- 1. Main target swapped normally into #item-list -->
<tr id="item-row-{{ new_item.pk }}">
    <td>{{ new_item.description }}</td>
    <td>{{ new_item.amount }}</td>
</tr>

<!-- 2. OOB Swap updates the summary counter in the header -->
<div id="invoice-total-badge" hx-swap-oob="true" class="badge-success">
    Total: ${{ invoice.calculate_total }}
</div>

<!-- 3. OOB Swap renders a temporary toast notification -->
<div id="toast-container" hx-swap-oob="beforeend">
    <div
        x-data="{ show: true }"
        x-show="show"
        x-init="setTimeout(() => show = false, 4000)"
        class="toast toast-success"
    >
        Line item added successfully!
    </div>
</div>
```

---

## 5. Inline Row Editing (Click-to-Edit Table Rows)

Allows editing a single row directly inside a table without opening a separate page.

### 5.1 Display Row (`_item_row.html`)
```html
<tr id="item-row-{{ item.pk }}">
    <td>{{ item.description }}</td>
    <td>${{ item.amount }}</td>
    <td class="text-right">
        <button
            type="button"
            hx-get="{% url 'billing:item-edit-row' item.pk %}"
            hx-target="#item-row-{{ item.pk }}"
            hx-swap="outerHTML"
            class="btn-sm btn-secondary"
        >
            Edit
        </button>
    </td>
</tr>
```

### 5.2 Edit Row Form (`_item_edit_row.html`)
```html
<tr id="item-row-{{ item.pk }}" class="bg-yellow-50">
    <td colspan="3">
        <form
            hx-post="{% url 'billing:item-edit-row' item.pk %}"
            hx-target="#item-row-{{ item.pk }}"
            hx-swap="outerHTML"
            class="flex items-center gap-2"
        >
            {% csrf_token %}
            <input type="text" name="description" value="{{ form.description.value }}" class="input-sm" />
            <input type="number" step="0.01" name="amount" value="{{ form.amount.value }}" class="input-sm w-24" />
            
            <button type="submit" class="btn-sm btn-success">Save</button>
            <button
                type="button"
                hx-get="{% url 'billing:item-display-row' item.pk %}"
                hx-target="#item-row-{{ item.pk }}"
                hx-swap="outerHTML"
                class="btn-sm btn-secondary"
            >
                Cancel
            </button>
        </form>
    </td>
</tr>
```

---

## 6. Infinite Scroll / Lazy Table Loading

Append records continuously as the user reaches the end of the viewport:

```html
<!-- Last row of the current page -->
{% for item in page_obj %}
    <tr>...</tr>
{% endfor %}

{% if page_obj.has_next %}
<tr
    hx-get="{% url 'billing:invoice-list-table' %}?page={{ page_obj.next_page_number }}"
    hx-trigger="revealed"
    hx-swap="afterend"
    class="htmx-indicator-row"
>
    <td colspan="4" class="text-center py-4">
        <span class="text-gray-500">Loading more invoices...</span>
    </td>
</tr>
{% endif %}
```

---

## 7. Integration with Other Skills

- **`htmx-alpine`**: Framework-agnostic principles and rules for when to use HTMX vs Alpine.
- **`htmx-patterns`**: Core Django conventions, headers (`HX-Request`), and CSRF handling.
- **`django-templates`**: Template inheritance, partial naming conventions (`_partial.html`).
- **`django-forms`**: Form validation, error display, and formsets.
