from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response

from tkrpl.auth import *
from main.utils import getHotelUser
from .models import *
from .forms import *
from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth import *

def list_room(request,hotel_name):
    hotel_choose=Hotel.objects.filter(name=hotel_name)[0]
    rooms=Room.objects.filter(hotel=hotel_choose, status="AVAILABLE")
    response={"rooms":rooms}
    return render(request,'room_list.html',response)

def book_room(request,hotel_name,room_name):
    if is_authenticated(request) != True | get_role(request) != "GUEST" |(get_role(request) == "GUEST" & request.user['guest_status']=='CHECK-IN') :
        return redirect(reverse_lazy("home"))
    else:
        if request.method == 'POST':
            form=BookRoomForm(request.POST)
            if form.is_valid():
                user=request.user
                hotel_stay=Hotel.objects.filter(name=hotel_name)[0]
                room=Room.objects.filter(hotel=hotel_stay,name=room_name)[0]
                start_date=datetime.today()
                end_date=request.POST['end_date']

                room_order=RoomOrder(order_date=start_date,end_date=end_date,guest=user,room=room)
                room_order.save()

                room_payment=RoomPayment(price=room.price,room_order=room_order)
                room_payment.save()

                room.status='OCCUPIED'
                room.save()

                user.guest_status='CHECK-IN'
                user.guest_current_stay=hotel_stay
                user.save()
                return HttpResponseRedirect('list_room/<str:hotel_name>/<str:room_name>')
        else:
            form=BookRoomForm(initial={'nama_kamar':room_name,'hotel_stay':hotel_name})
            return render(request,'book_room_form.html',{'form':form})

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
