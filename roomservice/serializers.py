from rest_framework import serializers
from .models import RoomService, RoomServiceOrder


class RoomServiceSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(source='hotel.name')

    class Meta:
        model = RoomService
        fields = ['id', 'type', 'name', 'img_url',
                  'status', 'price', 'hotel_name']


class RoomServiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomService
        fields = '__all__'


class RoomServiceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomServiceOrder
        fields = '__all__'
