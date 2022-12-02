from django.shortcuts import render
from asyncio.windows_events import NULL
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CreateRoomForm
from .models import Hotel
from room.models import Room,RoomOrder,RoomPayment
from accounts.models import HotelUser
from django.shortcuts import redirect

def create_room(request,hotel_name):
    if request.method == 'POST':
        form=CreateRoomForm(request.POST)
        if form.is_valid():
            hotel_choose=Hotel.objects.filter(name=hotel_name)[0]
            room=Room(name=request.POST['name'] ,kapasitas_max=request.POST['kapasitas_max'] ,tipe=request.POST['tipe'] ,status='AVAILABLE' ,hotel=hotel_choose)
            room.save(force_insert=True)
            return HttpResponseRedirect('/hotel/hotel_list')
    else:
        form =CreateRoomForm()
        response= {"create_room_form":form}
        return render(request,"create_room.html",response)

def list_room(request,hotel_name):
    hotel_choose=Hotel.objects.filter(name=hotel_name)[0]
    rooms=Room.objects.filter(hotel=hotel_choose,status='AVAILABLE')
    response={"rooms":rooms}
    return render(request,'room_list.html',response)

def book_room(request,hotel_name):
    if request.method == 'POST':
        return NULL
# Create your views here.
