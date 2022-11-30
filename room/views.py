from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from tkrpl.auth import *
from .models import *

# Create your views here.
def manage_rooms(request):
    if request.method != "POST":
        if get_role(request) != "HOTEL_SUPERVISOR":
            return redirect(reverse_lazy("home"))
        rooms = {
            "rooms": Room.objects.values()
        }
        return render(request, 'room/management.html', rooms)
    
    # return render(request, "room/create-edit.html")