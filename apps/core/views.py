from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST


@require_GET
def home_view(request: HttpRequest) -> HttpResponse:
    """Renders the landing page displaying HTMX, Alpine.js and DaisyUI."""
    counter = request.session.get("counter", 0)
    return render(request, "pages/home.html", {"counter": counter})


@require_POST
def htmx_counter_increment(request: HttpRequest) -> HttpResponse:
    """Demonstrates HTMX post request updating state and sending an OOB toast."""
    counter = request.session.get("counter", 0) + 1
    request.session["counter"] = counter
    return render(
        request,
        "pages/partials/_counter_box.html",
        {
            "counter": counter,
            "toast_message": f"Contador incrementado a {counter}!",
            "toast_type": "alert-success",
        },
    )


@require_POST
def htmx_counter_decrement(request: HttpRequest) -> HttpResponse:
    """Demonstrates HTMX post request decrementing counter."""
    counter = request.session.get("counter", 0) - 1
    request.session["counter"] = counter
    return render(
        request,
        "pages/partials/_counter_box.html",
        {
            "counter": counter,
            "toast_message": f"Contador decrementado a {counter}!",
            "toast_type": "alert-warning",
        },
    )


@require_GET
def htmx_modal_demo(request: HttpRequest) -> HttpResponse:
    """Demonstrates server-rendered modal partial loaded on demand."""
    return render(request, "pages/partials/_modal_demo.html")


@require_GET
def health_check(request: HttpRequest) -> JsonResponse:
    """Simple health check endpoint for container monitors or load balancers."""
    return JsonResponse({"status": "ok", "app": "django-starter-template"})
