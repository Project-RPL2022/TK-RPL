from asyncio.windows_events import NULL
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import HotelForm
from .models import Hotel
from room.models import Room,RoomOrder,RoomPayment
from accounts.models import HotelUser
from django.shortcuts import redirect

def hotel_register(request):
    if request.method == 'POST':
        form=HotelForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()  
            return HttpResponseRedirect('/hotel/hotel_list')
    else:
        form=HotelForm()
    return render(request,'hotel_form.html',{'form':form})

#buat daftarin/buat hotel baru dan buat kamar default 40 kamar/hotel

def hotel_list(request):
    hotels=Hotel.objects.all()
    response={"hotels":hotels}
    return render(request,'hotel_list.html',response)
#buat menunjukan daftar hotel infografis

def list_kamar(request):
    return NULL
#sees all alvailable room
#redirect to room/hotel_

def checkout():
    return NULL
#checkout dari hotel

