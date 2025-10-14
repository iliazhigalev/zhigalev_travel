from django.urls import path

from .views.booking_views import BookingDeleteView, BookingListCreateView
from .views.room_views import RoomDeleteView, RoomListCreateView

urlpatterns = [
    path("rooms/create", RoomListCreateView.as_view(), name="room-create"),
    path("rooms/delete", RoomDeleteView.as_view(), name="room-delete"),
    path("rooms/list", RoomListCreateView.as_view(), name="room-list"),
    path("bookings/create", BookingListCreateView.as_view(), name="booking-create"),
    path("bookings/delete", BookingDeleteView.as_view(), name="booking-delete"),
    path("bookings/list", BookingListCreateView.as_view(), name="booking-list"),
]
