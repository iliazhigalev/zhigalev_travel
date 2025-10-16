from rest_framework import serializers

from rooms.models.booking import Booking
from rooms.models.room import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "id",
            "number",
            "price_per_night",
            "is_available",
            "description",
            "created_at",
            "updated_at",
        )


class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("number", "price_per_night", "description", "is_available")


class BookingSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

    class Meta:
        model = Booking
        fields = ("id", "room", "check_in", "check_out", "created_at")


class BookingCreateSerializer(serializers.Serializer):
    room_id = serializers.IntegerField()
    date_start = serializers.DateField(input_formats=["%Y-%m-%d"])
    date_end = serializers.DateField(input_formats=["%Y-%m-%d"])

    def validate(self, data):
        if data["date_start"] >= data["date_end"]:
            raise serializers.ValidationError("date_end must be after date_start")
        try:
            room = Room.objects.get(id=data["room_id"])
        except Room.DoesNotExist:
            raise serializers.ValidationError("room_id not found")
        data["room"] = room
        return data

    def create(self, validated_data):
        return Booking.objects.create(
            room=validated_data["room"],
            check_in=validated_data["date_start"],
            check_out=validated_data["date_end"],
        )
