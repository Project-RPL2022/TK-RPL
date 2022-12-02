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
        form = CreateRoomForm()
        return render(request, 'room/create-room.html', {'form': form})

    form = CreateRoomForm(request.POST)
    if form.is_valid:
        form.save()
    return redirect(reverse_lazy("room-management"))


def edit_room(request):
    if request.method != "POST":
        form = CreateRoomForm()
        return render(request, 'room/create-room.html', {'form': form})

    # Display edit room
    try:
        id = request.POST['room']
        room = Room.objects.get(id=id)
        form = EditRoomForm(instance=room)
        return render(request, 'room/edit-room.html', {'form': form, 'id': id})
    except:
        pass

    # Save edit
    try:
        room = Room.objects.get(id=request.POST['id'])
        form = EditRoomForm(request.POST, instance=room)
        if form.is_valid:
            form.save()
        return redirect(reverse_lazy("room-management"))
    except:
        pass

    return redirect(reverse_lazy("room-management"))


class CheckoutView(APIView):
    def patch(self, request, format=None):
        hotel_user = getHotelUser(request.data["username"])

        hotel_user.guest_status = "CHECK-OUT"
        hotel_user.save()
        return Response({'msg': 'success'})
