import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory

from rooms.models.room import Room
from rooms.views.room_views import RoomDeleteView, RoomListCreateView


@pytest.mark.django_db
class TestRoomListCreateView:
    def setup_method(self):
        self.factory = APIRequestFactory()
        self.view = RoomListCreateView.as_view()

    def test_get_rooms_list(self):
        """Тест: получение списка номеров"""
        Room.objects.create(number=101, price_per_night=1000)
        Room.objects.create(number=102, price_per_night=1200)

        request = self.factory.get("/rooms/?sort_by=created_at&order=asc")
        response = self.view(request)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert {"id", "number", "price_per_night", "is_available", "description"}.issubset(
            response.data[0].keys()
        )

    def test_post_create_room_success(self):
        """Тест: успешное создание номера"""
        data = {
            "number": 105,
            "price_per_night": 1500,
            "is_available": True,
            "description": "Уютный номер",
        }
        request = self.factory.post("/rooms/", data, format="json")
        response = self.view(request)

        assert response.status_code == status.HTTP_201_CREATED
        assert "room_id" in response.data
        assert Room.objects.filter(number=105).exists()

    def test_post_create_room_invalid(self):
        """Тест: создание номера с невалидными данными"""
        data = {"price_per_night": 1000}  # пропущен number
        request = self.factory.post("/rooms/", data, format="json")
        response = self.view(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data


@pytest.mark.django_db
class TestRoomDeleteView:
    def setup_method(self):
        self.factory = APIRequestFactory()
        self.view = RoomDeleteView.as_view()

    def test_delete_room_success(self):
        """Тест: успешное удаление номера"""
        room = Room.objects.create(number=201, price_per_night=2000)
        request = self.factory.delete("/rooms/delete/", {"room_id": room.id}, format="json")
        response = self.view(request)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Room.objects.filter(id=room.id).exists()

    def test_delete_room_not_found(self):
        """Тест: удаление несуществующего номера"""
        request = self.factory.delete("/rooms/delete/", {"room_id": 999}, format="json")
        response = self.view(request)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"] == "Номер не найден"

    def test_delete_room_missing_id(self):
        """Тест: отсутствие room_id"""
        request = self.factory.delete("/rooms/delete/", {}, format="json")
        response = self.view(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "room_id required"
