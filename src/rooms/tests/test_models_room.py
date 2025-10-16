import pytest
from django.db import IntegrityError  # Добавьте этот импорт

from rooms.models.room import Room


@pytest.mark.django_db
def test_create_room():
    room = Room.objects.create(
        number="101",
        price_per_night=1500.00,
        description="Уютный номер с видом на море",
    )

    assert room.number == "101"
    assert float(room.price_per_night) == 1500.00
    assert room.is_available is True
    assert "101" in str(room)


@pytest.mark.django_db
def test_unique_room_number():
    Room.objects.create(number="202", price_per_night=1000.00)
    with pytest.raises(IntegrityError):
        Room.objects.create(number="202", price_per_night=1200.00)
