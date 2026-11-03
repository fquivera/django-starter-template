from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model inheriting from AbstractUser.
    Guarantees seamless schema evolution without migrations deadlocks.
    """

    bio = models.TextField(blank=True, default="")
    organization = models.CharField(max_length=150, blank=True, default="")

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.username
