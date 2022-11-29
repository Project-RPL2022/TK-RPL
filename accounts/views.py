from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from tkrpl.auth import *
from .forms import *
from .models import *

# Create your views here.

def signup(request):
    # Redirect next
    next = request.GET.get("next")
    if (next == None) or (next == "None"):
        next="/"

    if request.method != "POST":
        if is_authenticated(request):
            return redirect(reverse_lazy("login"))
        return render(request, 'registration/signup.html')
    
    # Save user
    try:
        user = User.objects.get(username=request.POST['username'])
    except:
        user = User.objects.create_user(request.POST['username'],"",request.POST['password'])
        user.save()

    try:
        hoteluser = HotelUser.objects.get(user=user)
        return redirect(reverse_lazy("signup"))
    except:
        hoteluser = HotelUser(user=user,role=request.POST['role'])
        hoteluser.save()

    return redirect(reverse_lazy("login"))