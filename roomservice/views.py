from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User
from accounts.models import HotelUser

from .models import RoomService
from .serializers import RoomServiceSerializer, RoomServiceDetailSerializer


class RoomServiceDetail(APIView):
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
