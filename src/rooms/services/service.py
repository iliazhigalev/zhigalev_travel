# rooms/services.py
from django.core.exceptions import ObjectDoesNotExist

from ..models import Booking, Room


def create_room(data):
    room = Room.objects.create(
        number=data["number"],
        price_per_night=data["price_per_night"],
        is_available=data.get("is_available", True),
        description=data.get("description", ""),
    )
    return room


def list_rooms(sort_by="created_at", order="asc"):
    if sort_by not in ["price", "created_at"]:
        sort_by = "created_at"
    if order == "desc":
        sort_by = f"-{sort_by}"
    return Room.objects.all().order_by(sort_by)


def delete_room(room_id):
    try:
        room = Room.objects.get(id=room_id)
        room.delete()
        return True
    except ObjectDoesNotExist:
        return False


def create_booking(data):
    try:
        room = data["room"]
    except ObjectDoesNotExist:
        raise ValueError("Room not found")
    return Booking.objects.create(room=room, check_in=data["check_in"], check_out=data["check_out"])


def list_bookings(room_id: int):
    if not room_id:
        raise ValueError("room_id required")
    return Booking.objects.filter(room_id=room_id).order_by("check_in")


def delete_booking(booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        booking.delete()
        return True
    except ObjectDoesNotExist:
        return False
