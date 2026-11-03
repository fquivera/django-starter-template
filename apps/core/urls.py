from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home_view, name="home"),
    path(
        "htmx/counter/increment/",
        views.htmx_counter_increment,
        name="counter-increment",
    ),
    path(
        "htmx/counter/decrement/",
        views.htmx_counter_decrement,
        name="counter-decrement",
    ),
    path("htmx/modal-demo/", views.htmx_modal_demo, name="modal-demo"),
    path("health/", views.health_check, name="health-check"),
]
