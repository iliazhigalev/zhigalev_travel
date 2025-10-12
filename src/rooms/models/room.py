from django.db import models


class Room(models.Model):
    number = models.CharField(max_length=10, unique=True, verbose_name="Номер комнаты")
    price_per_night = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Цена за ночь"
    )
    is_available = models.BooleanField(default=True, verbose_name="Доступна для бронирования")
    description = models.TextField(blank=True, verbose_name="Описание")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"
        ordering = ["number"]

    def __str__(self):
        return f"Комната номер № {self.number}"
