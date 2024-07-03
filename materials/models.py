from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название курса", help_text="Введите название курса")
    preview = models.ImageField(upload_to="materials/preview ", verbose_name="Превью", help_text="Загрузить превью", **NULLABLE)
    description = models.TextField(verbose_name="Описание", **NULLABLE)


    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return f"{self.name}"
