from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from tkrpl.auth import *
from .models import *
from .forms import *

# Create your views here.
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
        return render(request, 'room/create-room.html', {'form' : form})