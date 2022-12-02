from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from tkrpl.auth import *
from .models import *
from .forms import *

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
        return render(request, 'room/create-room.html', {'form' : form})
    
    form = CreateRoomForm(request.POST)
    if form.is_valid:
        form.save()
    return redirect(reverse_lazy("room-management"))

def edit_room(request):
    if request.method != "POST":
        form = CreateRoomForm()
        return render(request, 'room/create-room.html', {'form' : form})
    
    # Display edit room
    try:
        id=request.POST['room']
        room = Room.objects.get(id=id)
        form = EditRoomForm(instance=room)
        return render(request, 'room/edit-room.html', {'form':form, 'id':id})
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