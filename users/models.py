from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _



NULLABLE = {"blank": True, "null": True}

# Create your models here.
class UserRoles(models.TextChoices):
    ADMIN = 'admin', _('admin')
    MODERATOR = 'moderator', _('moderator')
    USER = 'user', _('user')


class User(AbstractUser):
    username = models.CharField(max_length=150, verbose_name="имя", **NULLABLE)
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.USER)
    email = models.EmailField(unique=True, verbose_name="Эл. почта")


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['id']
