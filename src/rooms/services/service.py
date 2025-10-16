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
    if sort_by == "price":
        sort_by = "price_per_night"
    elif sort_by not in ["price_per_night", "created_at"]:
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
    room_id = data.get("room_id") or data.get("room")
    date_start = data["date_start"]
    date_end = data["date_end"]

    room = Room.objects.filter(id=room_id).first()
    if not room:
        raise ValueError("Номер не найден")

    if date_end <= date_start:
        raise ValueError("Дата выезда должна быть позже даты заезда")

    booking = Booking.objects.create(
        room=room,
        check_in=date_start,
        check_out=date_end,
    )
    return booking


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
