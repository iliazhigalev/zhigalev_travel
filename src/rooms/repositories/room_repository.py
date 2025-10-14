from rooms.models.room import Room


class RoomRepository:
    @staticmethod
    def create(description: str, price: float) -> Room:
        """Добавление номера отеля"""

        return Room.objects.create(description=description, price=price)

    @staticmethod
    def delete(room_id: int) -> bool:
        """
        Удалить номер отеля и все его брони
        Возвращает True, если удалено и False в противном случае
        """

        deleted_count, _ = Room.objects.filter(id=room_id).delete()
        return deleted_count > 0

    @staticmethod
    def list(order_by: str = "created_at"):
        "Получение списка номеров отеля"
        return Room.objects.all().order_by(order_by)
