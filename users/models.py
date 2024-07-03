from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}

class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Введите email")
    phone = models.CharField(
        max_length=35, verbose_name="Телефон", help_text="Введите телефон", **NULLABLE
    )
    city = models.CharField(max_length=100, verbose_name="Город", help_text="Введите город проживания", **NULLABLE
    )
    avatar = models.ImageField(upload_to="users/avatars", verbose_name="Аватар", help_text="Загрузите аватар")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []