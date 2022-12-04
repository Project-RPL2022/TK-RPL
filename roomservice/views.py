import json
from datetime import datetime

from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User
from accounts.models import HotelUser
from main.utils import getHotelUser

from .models import RoomService, RoomServiceOrder
from .serializers import RoomServiceSerializer, RoomServiceDetailSerializer, RoomServiceOrderSerializer


class RoomServiceDetailView(APIView):
    def get_object(self, pk):
        try:
            return RoomService.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk, format=None):
        room_service = self.get_object(pk)
        serializer = RoomServiceDetailSerializer(room_service)
        return Response(serializer.data)


class RoomServiceView(APIView):

    def get(self, request, format=None):
        # check user
        if not request.user.is_authenticated:
            raise PermissionDenied(
                {"error_message": "You don't have permission to access"})

        user = User.objects.get(username=request.user)
        hotel_user = HotelUser.objects.get(user=user)

        # check stay-in
        if hotel_user.guest_status != 'CHECK-IN':
            raise PermissionDenied(
                {"error_message": "You don't have permission to access"})

        room_services = RoomService.objects.filter(
            hotel=hotel_user.guest_current_stay)
        serializer = RoomServiceSerializer(room_services, many=True)
        return Response({'data': serializer.data})


class RoomServiceOrderView(APIView):
    def get(self, request, format=None):
        hotel_user = getHotelUser(request.user)

        orders = RoomServiceOrder.objects.filter(guest=hotel_user)
        serializer = RoomServiceOrderSerializer(orders, many=True)
        return Response({'data': serializer.data})

    def post(self, request, format=None):
        user = User.objects.get(username=request.user)
        time_now = datetime.now()
        time_served = request.data.get('time_served', time_now)
        notes = request.data.get('notes', "-")

        hotel_user = HotelUser.objects.get(user=user)
        room_service = RoomService.objects.get(
            pk=request.data['room_service_id'])

        order = RoomServiceOrder.objects.create(
            notes=notes,
            time_served=time_served,
            order_date=time_now,
            room_service=room_service,
            guest=hotel_user
        )
        serializer = RoomServiceOrderSerializer(order)
        return Response({'data': serializer.data})

    def patch(self, request, format=None):
        order = RoomServiceOrder.objects.get(pk=request.data["order_id"])
        order.status = request.data["status"]
        order.save()
        serializer = RoomServiceOrderSerializer(order)
        return Response({'data': serializer.data})
