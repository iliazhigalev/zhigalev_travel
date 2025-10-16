import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory

from rooms.models.booking import Booking
from rooms.models.room import Room
from rooms.views.booking_views import BookingDeleteView, BookingListCreateView


@pytest.mark.django_db
class TestBookingListCreateView:
    def setup_method(self):
        self.factory = APIRequestFactory()
        self.view = BookingListCreateView.as_view()
        self.room = Room.objects.create(number="301", price_per_night=2000)

    def test_get_bookings_success(self):
        """Тест: успешное получение списка броней по room_id"""
        Booking.objects.create(room=self.room, check_in="2025-10-20", check_out="2025-10-25")
        Booking.objects.create(room=self.room, check_in="2025-11-01", check_out="2025-11-03")

        request = self.factory.get(f"/bookings/?room_id={self.room.id}")
        response = self.view(request)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert "check_in" in response.data[0]

    def test_get_bookings_missing_room_id(self):
        """Тест: ошибка при отсутствии room_id"""
        request = self.factory.get("/bookings/")
        with pytest.raises(ValueError, match="room_id required"):
            self.view(request)

    def test_post_create_booking_success(self):
        """Тест: успешное создание брони"""
        data = {
            "room_id": self.room.id,
            "date_start": "2025-11-01",
            "date_end": "2025-11-03",
        }
        request = self.factory.post("/bookings/", data, format="json")
        response = self.view(request)
        print(response.data)

        assert response.status_code == status.HTTP_201_CREATED
        assert "booking_id" in response.data
        assert Booking.objects.filter(id=response.data["booking_id"]).exists()

    def test_post_create_booking_invalid_dates(self):
        """Тест: ошибка валидации — check_out раньше check_in"""
        data = {
            "room": self.room.id,
            "check_in": "2025-12-05",
            "check_out": "2025-12-01",
        }
        request = self.factory.post("/bookings/", data, format="json")
        response = self.view(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data

    def test_post_create_booking_room_not_found(self):
        """Тест: попытка создать бронь для несуществующего номера"""
        data = {
            "room": 9999,
            "check_in": "2025-12-10",
            "check_out": "2025-12-12",
        }
        request = self.factory.post("/bookings/", data, format="json")
        response = self.view(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data


@pytest.mark.django_db
class TestBookingDeleteView:
    def setup_method(self):
        self.factory = APIRequestFactory()
        self.view = BookingDeleteView.as_view()
        self.room = Room.objects.create(number="401", price_per_night=2500)
        self.booking = Booking.objects.create(
            room=self.room, check_in="2025-10-15", check_out="2025-10-17"
        )

    def test_delete_booking_success(self):
        """Тест: успешное удаление существующей брони"""
        request = self.factory.delete(
            "/bookings/delete/", {"booking_id": self.booking.id}, format="json"
        )
        response = self.view(request)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Booking.objects.filter(id=self.booking.id).exists()

    def test_delete_booking_not_found(self):
        """Тест: удаление несуществующей брони"""
        request = self.factory.delete("/bookings/delete/", {"booking_id": 9999}, format="json")
        response = self.view(request)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"] == "Бронь не найдена"

    def test_delete_booking_missing_id(self):
        """Тест: удаление без передачи booking_id"""
        request = self.factory.delete("/bookings/delete/", {}, format="json")
        response = self.view(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "booking_id required"
