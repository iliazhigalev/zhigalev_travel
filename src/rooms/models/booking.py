from django.db import models

from .room import Room


class Booking(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="bookings", verbose_name="Номер"
    )
    check_in = models.DateField(verbose_name="Дата заезда")
    check_out = models.DateField(verbose_name="Дата выезда")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Бронь комнаты {self.room.number} c {self.check_in} по {self.check_out}"

    def save(self, *args, **kwargs):
        # Простейшая бизнес-логика: проверка дат
        if self.check_in >= self.check_out:
            raise ValueError("Дата выезда должна быть позже даты заезда.")
        super().save(*args, **kwargs)
