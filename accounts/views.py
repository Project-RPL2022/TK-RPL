from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from tkrpl.auth import *
from .models import *

# Create your views here.
roles = {'GUEST':'Guest',
        'HOTEL_SUPERVISOR':'Hotel Supervisor',
        'HOTEL_ADMINISTRATOR': 'Hotel Administrator'}

def signup(request):
    # Redirect next
    next = request.GET.get("next")
    if (next == None) or (next == "None"):
        next="/"

    if request.method != "POST":
        if request.user.is_anonymous:
            return render(request, 'registration/signup.html', {'roles':roles})
        return redirect(reverse_lazy("home"))
    
    # Save user
    try:
        currentuser = User.objects.get(username=request.POST['username'])
    except:
        currentuser = User.objects.create_user(
            username=request.POST['username'],
            first_name=request.POST['first_name'],
            email="",
            password=request.POST['password'])
        currentuser.save()

    if HotelUser.objects.filter(user=currentuser).exists():
        message = "Username already taken."
        return render(request, 'registration/signup.html', {
            "message":message,
            "username":request.POST['username'],
            "first_name":request.POST['first_name'],
            "password":request.POST['password'],
            "prevrole":request.POST['role'],
            'roles':roles
            })
    else:
        hoteluser = HotelUser(user=currentuser,role=request.POST['role'])
        hoteluser.save()
    
    return redirect(reverse_lazy("login"))