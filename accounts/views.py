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

    userdata = request.POST
    
    # Save user
    try:
        user = User.objects.create_user(userdata['username'],"",userdata['password'])
        user.save()
    except:
        user = User.objects.get(username=userdata['username'])
    
    try:
        hoteluser = HotelUser(user=user,role="GUEST")
        hoteluser.save()
    except:
        hoteluser = HotelUser.objects.get(user=user)
    
    return redirect(reverse_lazy("login"))