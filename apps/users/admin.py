from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "organization",
        "is_staff",
    )
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "first_name", "last_name", "organization")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Información Adicional", {"fields": ("bio", "organization")}),
    )
