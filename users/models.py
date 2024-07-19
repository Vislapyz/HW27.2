from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Введите email"
    )
    phone = models.CharField(
        max_length=35, verbose_name="Телефон", help_text="Введите телефон", **NULLABLE
    )
    city = models.CharField(
        max_length=100,
        verbose_name="Город",
        help_text="Введите город проживания",
        **NULLABLE,
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        help_text="Загрузите аватар",
        **NULLABLE,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    course = models.ForeignKey(
        Course, verbose_name="Курс", on_delete=models.CASCADE, blank=True, null=True
    )
    lesson = models.ForeignKey(
        Lesson,
        verbose_name="Урок",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    total_price = models.FloatField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(max_length=50, verbose_name="Способ оплаты")
    session_id = models.CharField(max_length=255, verbose_name="ID сессии",
                                  help_text='Укажите ID Сессии', **NULLABLE)
    payment_link = models.URLField(max_length=400, verbose_name="Ссылка на оплату",
                           help_text='Укажите ссылку на оплату', **NULLABLE)

    def __str__(self):
        return (
            f"{self.user} - {self.course if self.course else self.lesson} = "
            f"{self.total_price}$"
        )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
