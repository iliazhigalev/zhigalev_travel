from datetime import date, timedelta

import pytest
from django.core.exceptions import ValidationError

from rooms.models.booking import Booking
from rooms.models.room import Room


@pytest.mark.django_db
def test_create_booking():
    room = Room.objects.create(number="303", price_per_night=2000.00)
    booking = Booking.objects.create(
        room=room,
        check_in=date.today(),
        check_out=date.today() + timedelta(days=2),
    )

    assert booking.room == room
    assert booking.check_out > booking.check_in
    assert "303" in str(booking)


@pytest.mark.django_db
def test_booking_date_validation():
    room = Room.objects.create(number="404", price_per_night=2500.00)
    booking = Booking(
        room=room,
        check_in=date.today(),
        check_out=date.today(),
    )

    with pytest.raises(ValidationError):
        booking.clean()


@pytest.mark.django_db
def test_booking_ordering():
    room = Room.objects.create(number="505", price_per_night=1800.00)
    Booking.objects.create(
        room=room,
        check_in=date.today(),
        check_out=date.today() + timedelta(days=1),
    )
    Booking.objects.create(
        room=room,
        check_in=date.today() + timedelta(days=2),
        check_out=date.today() + timedelta(days=3),
    )

    all_bookings = list(Booking.objects.all())
    assert all_bookings[0].created_at >= all_bookings[1].created_at
