from datetime import date

import pytest

from rooms.models import Booking, Room
from rooms.serializers import (
    BookingCreateSerializer,
    BookingSerializer,
    RoomCreateSerializer,
    RoomSerializer,
)


@pytest.mark.django_db
class TestRoomSerializer:
    def test_room_serializer_fields(self):
        room = Room.objects.create(
            number="101",
            price_per_night=1500,
            is_available=True,
            description="Nice sea view",
        )

        serializer = RoomSerializer(room)
        data = serializer.data

        assert set(data.keys()) == {
            "id",
            "number",
            "price_per_night",
            "is_available",
            "description",
            "created_at",
            "updated_at",
        }
        assert data["number"] == "101"
        assert data["price_per_night"] == "1500.00"
        assert data["is_available"] is True


@pytest.mark.django_db
class TestRoomCreateSerializer:
    def test_room_create_serializer_valid(self):
        data = {
            "number": "202",
            "price_per_night": 1800,
            "description": "With balcony",
            "is_available": False,
        }

        serializer = RoomCreateSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

        room = serializer.save()
        assert Room.objects.count() == 1
        assert room.number == "202"
        assert room.price_per_night == 1800
        assert room.is_available is False

    def test_room_create_serializer_missing_field(self):
        data = {"number": "303"}
        serializer = RoomCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "price_per_night" in serializer.errors


@pytest.mark.django_db
class TestBookingSerializer:
    def test_booking_serializer_output(self):
        room = Room.objects.create(
            number="401",
            price_per_night=2500,
            is_available=True,
            description="Test room",
        )
        booking = Booking.objects.create(
            room=room,
            check_in=date(2025, 11, 1),
            check_out=date(2025, 11, 5),
        )

        serializer = BookingSerializer(booking)
        data = serializer.data

        assert data["room"] == room.id
        assert data["check_in"] == "2025-11-01"
        assert data["check_out"] == "2025-11-05"


@pytest.mark.django_db
class TestBookingCreateSerializer:
    def test_booking_create_valid(self):
        room = Room.objects.create(
            number="501",
            price_per_night=3000,
            is_available=True,
            description="Luxury",
        )
        data = {
            "room_id": room.id,
            "date_start": date(2025, 12, 1),
            "date_end": date(2025, 12, 5),
        }

        serializer = BookingCreateSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

        booking = serializer.save()
        assert Booking.objects.count() == 1
        assert booking.room == room
        assert booking.check_in == date(2025, 12, 1)
        assert booking.check_out == date(2025, 12, 5)

    def test_booking_create_invalid_dates(self):
        room = Room.objects.create(
            number="502",
            price_per_night=3000,
            is_available=True,
            description="Invalid date test",
        )
        data = {
            "room_id": room.id,
            "date_start": date(2025, 12, 5),
            "date_end": date(2025, 12, 1),
        }

        serializer = BookingCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "date_end must be after date_start" in str(serializer.errors)

    def test_booking_create_invalid_room(self):
        data = {
            "room_id": 9999,  # несуществующий ID
            "date_start": date(2025, 12, 1),
            "date_end": date(2025, 12, 3),
        }

        serializer = BookingCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "room_id not found" in str(serializer.errors)
