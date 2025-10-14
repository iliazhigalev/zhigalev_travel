from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.serializers import RoomSerializer
from ..services.service import create_room, delete_room, list_rooms


class RoomListCreateView(APIView):
    """
    GET: получить список номеров с сортировкой
    POST: создать новый номер
    """

    def get(self, request):
        sort_by = request.query_params.get("sort_by", "created_at")
        order = request.query_params.get("order", "asc")
        rooms = list_rooms(sort_by, order)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            room = create_room(serializer.validated_data)
            return Response({"room_id": room.id}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RoomDeleteView(APIView):
    def delete(self, request):
        room_id = request.data.get("room_id") or request.query_params.get("room_id")
        if not room_id:
            return Response({"error": "room_id required"}, status=status.HTTP_400_BAD_REQUEST)
        success = delete_room(room_id)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Номер не найден"}, status=status.HTTP_404_NOT_FOUND)
