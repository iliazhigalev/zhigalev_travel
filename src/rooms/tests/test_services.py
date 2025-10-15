from datetime import date, timedelta

import pytest

from rooms.models import Booking, Room
from rooms.services import service as services


@pytest.mark.django_db
def test_create_room():
    data = {"number": "101", "price_per_night": 2500}
    room = services.create_room(data)

    assert isinstance(room, Room)
    assert room.number == "101"
    assert room.price_per_night == 2500
    assert room.is_available is True
    assert room.description == ""


@pytest.mark.django_db
def test_list_rooms_sorting():
    # Создаём комнаты с разной ценой
    r1 = Room.objects.create(number="201", price_per_night=1000)
    r2 = Room.objects.create(number="202", price_per_night=3000)
    r3 = Room.objects.create(number="203", price_per_night=2000)

    rooms_asc = services.list_rooms(sort_by="price", order="asc")
    rooms_desc = services.list_rooms(sort_by="price", order="desc")

    assert list(rooms_asc) == [r1, r3, r2]
    assert list(rooms_desc) == [r2, r3, r1]


@pytest.mark.django_db
def test_delete_room_success():
    room = Room.objects.create(number="301", price_per_night=1000)
    result = services.delete_room(room.id)
    assert result is True
    assert Room.objects.count() == 0


@pytest.mark.django_db
def test_delete_room_not_found():
    result = services.delete_room(9999)
    assert result is False


@pytest.mark.django_db
def test_create_booking_success():
    room = Room.objects.create(number="401", price_per_night=1800)
    data = {
        "room_id": room.id,
        "date_start": date.today(),
        "date_end": date.today() + timedelta(days=2),
    }
    booking = services.create_booking(data)

    assert isinstance(booking, Booking)
    assert booking.room == room
    assert booking.check_out > booking.check_in


@pytest.mark.django_db
def test_create_booking_room_not_found():
    with pytest.raises(ValueError):
        services.create_booking(
            {
                "room_id": 9999,  # Комнаты с таким id нет
                "date_start": date.today(),
                "date_end": date.today() + timedelta(days=2),
            }
        )


@pytest.mark.django_db
def test_list_bookings_success():
    room = Room.objects.create(number="501", price_per_night=1200)
    b1 = Booking.objects.create(room=room, check_in=date(2025, 1, 1), check_out=date(2025, 1, 3))
    b2 = Booking.objects.create(room=room, check_in=date(2025, 1, 5), check_out=date(2025, 1, 7))

    bookings = services.list_bookings(room.id)
    assert list(bookings) == [b1, b2]


@pytest.mark.django_db
def test_list_bookings_missing_room_id():
    with pytest.raises(ValueError):
        services.list_bookings(None)


@pytest.mark.django_db
def test_delete_booking_success():
    room = Room.objects.create(number="601", price_per_night=2000)
    booking = Booking.objects.create(
        room=room, check_in=date.today(), check_out=date.today() + timedelta(days=1)
    )

    result = services.delete_booking(booking.id)
    assert result is True
    assert Booking.objects.count() == 0


@pytest.mark.django_db
def test_delete_booking_not_found():
    result = services.delete_booking(9999)
    assert result is False
