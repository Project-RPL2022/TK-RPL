from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response

from tkrpl.auth import *
from main.utils import getHotelUser
from .models import *
from .forms import *


def manage_rooms(request):
    if request.method != "POST":
        if get_role(request) != "HOTEL_SUPERVISOR":
            return redirect(reverse_lazy("home"))
        rooms = {
            "rooms": Room.objects.all()
        }
        return render(request, 'room/management.html', rooms)


def create_room(request):
    if request.method != "POST":
        form = RoomForm()
        return render(request, 'room/create-room.html', {'form': form})


class CheckoutView(APIView):
    def patch(self, request, format=None):
        hotel_user = getHotelUser(request.data["username"])

        hotel_user.guest_status = "CHECK-OUT"
        hotel_user.save()
        return Response({'msg': 'success'})
