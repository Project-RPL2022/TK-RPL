import json
from datetime import datetime

from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User
from accounts.models import HotelUser
from hotel.models import Hotel
from main.utils import getHotelUser

from .models import RoomService, RoomServiceOrder
from .serializers import RoomServiceSerializer, RoomServiceDetailSerializer, RoomServiceOrderSerializer

default_img = "https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg"


class RoomServiceDetailView(APIView):
    def get_object(self, pk):
        try:
            return RoomService.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk, format=None):
        room_service = self.get_object(pk)
        serializer = RoomServiceDetailSerializer(room_service)
        return Response(
            {
                'data': serializer.data,
                'additionalData': {
                    'hotel_name': room_service.hotel.name
                }
            }
        )


class RoomServiceView(APIView):
    def get(self, request, format=None):
        # check user
        if not request.user.is_authenticated:
            raise PermissionDenied(
                {"error_message": "You don't have permission to access"})

        user = User.objects.get(username=request.user)
        hotel_user = HotelUser.objects.get(user=user)
        role = hotel_user.role

        if role == 'GUEST':
            current_hotel = hotel_user.guest_current_stay
        else:
            current_hotel = hotel_user.works_at

        # check stay-in
        if hotel_user.guest_status != 'CHECK-IN' and role == 'GUEST':
            raise PermissionDenied(
                {"error_message": "You don't have permission to access"})

        room_services = RoomService.objects.filter(
            hotel=current_hotel).order_by("status", "type")

        serializer = RoomServiceSerializer(room_services, many=True)

        hotel = hotel_user.guest_current_stay
        additionalData = {}
        if hotel != None:
            additionalData = {'hotel_name': hotel.name}
        else:
            raise PermissionDenied(
                {"error_message": "You don't have permission to access"})

        return Response({'data': serializer.data, 'additionalData': additionalData})

    def post(self, request, format=None):
        user = User.objects.get(username=request.user)
        hotel_user = HotelUser.objects.get(user=user)

        type = request.data.get('type', '-')
        name = request.data.get('name', '-')
        img_url = request.data.get('img_url', default_img)
        price = request.data.get('price', 0)
        hotel = hotel_user.works_at

        room_service = RoomService.objects.create(
            type=type,
            name=name,
            img_url=img_url,
            price=price,
            hotel=hotel
        )

        serializer = RoomServiceSerializer(room_service)
        return Response({'data': serializer.data, 'msg': 'Success'})


class RoomServiceUpdateView(APIView):
    def post(self, request, format=None):
        room = RoomService.objects.get(pk=request.data["room_id"])
        room.type = request.data["type"]
        room.name = request.data["name"]
        room.img_url = request.data["img_url"]
        room.price = request.data["price"]
        room.save()
        serializer = RoomServiceSerializer(room)
        return Response({'data': serializer.data})


class RoomServiceOrderDetailView(APIView):
    def get_object(self, pk):
        try:
            return RoomServiceOrder.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk, format=None):
        room_service_order = self.get_object(pk)
        serializer = RoomServiceOrderSerializer(room_service_order)
        return Response(
            {
                'data': serializer.data,
            }
        )


class RoomServiceOrderView(APIView):
    def get(self, request, format=None):
        hotel_user = getHotelUser(request.user)

        if hotel_user.role == 'GUEST':
            orders = RoomServiceOrder.objects.filter(guest=hotel_user)
        else:
            orders = RoomServiceOrder.objects.all()
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


class RoomServiceOrderUpdateView(APIView):
    def post(self, request, format=None):
        order = RoomServiceOrder.objects.get(pk=request.data["order_id"])
        order.status = request.data["status"]
        order.save()
        serializer = RoomServiceOrderSerializer(order)
        return Response({'data': serializer.data})

# pages


class RoomServicePage(APIView):
    def get(self, request, format=None):
        # check user
        if not request.user.is_authenticated:
            raise PermissionDenied(
                {"error_message": "You don't have permission to access"})

        user = User.objects.get(username=request.user)
        hotel_user = HotelUser.objects.get(user=user)

        # check stay-in
        if hotel_user.guest_status != 'CHECK-IN':
            return render(request, 'room_services/redirect.html')

        return render(
            request,
            'room_services/index.html',
            {
                'role': hotel_user.role
            }
        )


class RoomServiceAddPage(APIView):
    def get(self, request, format=None):
        # check user
        if not request.user.is_authenticated:
            raise PermissionDenied(
                {"error_message": "You don't have permission to access"})

        user = User.objects.get(username=request.user)
        hotel_user = HotelUser.objects.get(user=user)

        # check stay-in
        if hotel_user.role == 'GUEST':
            return render(request, 'home.html')

        return render(
            request,
            'room_services/add/index.html'
        )


class RoomServiceUpdatePage(APIView):
    def get(self, request, pk, format=None):
        # check user
        if not request.user.is_authenticated:
            raise PermissionDenied(
                {"error_message": "You don't have permission to access"})

        user = User.objects.get(username=request.user)
        hotel_user = HotelUser.objects.get(user=user)

        # check stay-in
        if hotel_user.role == 'GUEST':
            return render(request, 'home.html')

        return render(
            request,
            'room_services/update/index.html'
        )


class RoomServiceDetailPage(APIView):
    def get(self, request, pk, format=None):
        # check user
        if not request.user.is_authenticated:
            raise PermissionDenied(
                {"error_message": "You don't have permission to access"})

        user = User.objects.get(username=request.user)
        hotel_user = HotelUser.objects.get(user=user)

        # check stay-in
        if hotel_user.guest_status != 'CHECK-IN':
            return render(request, 'room_services/redirect.html')

        return render(request, 'room_services/detail/index.html')


class RoomServiceOrderPage(APIView):
    def get(self, request, format=None):
        # check user
        if not request.user.is_authenticated:
            raise PermissionDenied(
                {"error_message": "You don't have permission to access"})

        user = User.objects.get(username=request.user)
        hotel_user = HotelUser.objects.get(user=user)
        role = hotel_user.role

        return render(request, 'room_services_order/index.html', {'role': role})


class RoomServiceOrderDetailPage(APIView):
    def get(self, request, pk, format=None):
        # check user
        if not request.user.is_authenticated:
            raise PermissionDenied(
                {"error_message": "You don't have permission to access"})

        user = User.objects.get(username=request.user)
        hotel_user = HotelUser.objects.get(user=user)
        role = hotel_user.role

        return render(request, 'room_services_order/detail/index.html', {'role': role})
