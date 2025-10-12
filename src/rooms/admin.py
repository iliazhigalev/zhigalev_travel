from django.contrib import admin

from .models import Booking, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("number", "price_per_night", "is_available", "created_at")
    list_filter = ("is_available",)
    search_fields = ("number", "description")
    ordering = ("number",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("room", "check_in", "check_out", "created_at")
    list_filter = ("check_in", "check_out", "room")
    search_fields = ("room__number",)
