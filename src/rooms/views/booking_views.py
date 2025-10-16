from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import BookingCreateSerializer, BookingSerializer
from ..services import create_booking, delete_booking, list_bookings


class BookingListCreateView(APIView):
    """
    GET: список броней по ID комнаты
    POST: создать новую бронь
    """

    def get(self, request):
        room_id = request.query_params.get("room_id")
        if room_id is None:
            raise ValueError("room_id required")

        room_id = int(room_id)
        try:
            bookings = list_bookings(room_id)
            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                booking = create_booking(serializer.validated_data)
                return Response({"booking_id": booking.id}, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class BookingDeleteView(APIView):
    def delete(self, request):
        booking_id = request.data.get("booking_id") or request.query_params.get("booking_id")
        if not booking_id:
            return Response({"error": "booking_id required"}, status=status.HTTP_400_BAD_REQUEST)
        success = delete_booking(booking_id)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Бронь не найдена"}, status=status.HTTP_404_NOT_FOUND)
