from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from tkrpl.auth import *
from main.utils import getHotelUser
from .models import *
from .forms import *
from .serializer import *
from room.models import *
from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required


def list_room(request, hotel_name):
    hotel_choose = Hotel.objects.filter(name=hotel_name)[0]
    rooms = Room.objects.filter(hotel=hotel_choose, status="AVAILABLE")
    response = {"rooms": rooms}
    return render(request, 'room_list.html', response)


def book_room(request, hotel_name, room_name):
    if request.user.is_anonymous | (get_role(request) != "GUEST"):
        return redirect(reverse_lazy("home"))
    else:
        user = request.user
        hoteluser = HotelUser.objects.get(user=user)
        if (hoteluser.guest_status != "CHECK-OUT"):
            return HttpResponseRedirect('list_room/<str:hotel_name>')

        hotel_stay = Hotel.objects.filter(name=hotel_name)[0]
        room_stay = Room.objects.filter(hotel=hotel_stay, name=room_name)[0]
        if request.method == 'POST':
            form = BookRoomForm(request.POST)
            if form.is_valid():

                room_order = form.save()

                room_payment = RoomPayment(
                    price=room_stay.price, room_order=room_order)
                room_payment.save()

                room_stay.status = 'OCCUPIED'
                room_stay.save()

                hoteluser.guest_status = 'CHECK-IN'
                hoteluser.guest_current_stay = hotel_stay
                hoteluser.save()
                return redirect('/room/list_room/'+hotel_name)

        else:
            initial_data = {
                'guest': hoteluser,
                'room': room_stay
            }
            form = BookRoomForm(initial=initial_data)
            return render(request, 'book_room_form.html', {'form': form})


@login_required
def manage_rooms(request):
    if get_role(request) != "HOTEL_SUPERVISOR":
        return redirect(reverse_lazy("home"))
    if request.method != "POST":
        context = {
            "rooms": Room.objects.all(),
            "role": get_role(request)
        }
        return render(request, 'room/management.html', context)


@login_required
def create_room(request):
    if get_role(request) != "HOTEL_SUPERVISOR":
        return redirect(reverse_lazy("home"))
    if request.method != "POST":
        form = CreateRoomForm()
        return render(request, 'room/create-room.html', {'form': form, "role": get_role(request)})

    form = CreateRoomForm(request.POST)
    if form.is_valid:
        form.save()
    return redirect(reverse_lazy("room-management"))


@login_required
def edit_room(request):
    if get_role(request) != "HOTEL_SUPERVISOR":
        return redirect(reverse_lazy("home"))
    if request.method != "POST":
        form = CreateRoomForm()
        return render(request, 'room/create-room.html', {'form': form, "role": get_role(request)})

    # Display edit room
    try:
        id = request.POST['room']
        room = Room.objects.get(id=id)
        form = EditRoomForm(instance=room)
        return render(request, 'room/edit-room.html', {'form': form, 'id': id, "role": get_role(request)})
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
    def get(self, request, format=None):
        supervisor = getHotelUser(request.user)

        users = HotelUser.objects.filter(
            guest_current_stay=supervisor.works_at).order_by('guest_status')
        serializer = CheckoutListSerializer(users, many=True)

        return Response({'data': serializer.data})

    def post(self, request, format=None):
        hotel_user = getHotelUser(request.data["username"])

        # change state
        hotel_user.guest_status = "CHECK-OUT"
        hotel_user.save()

        # end date for order
        room_order = RoomOrder.objects.get(
            guest=hotel_user,
            status="OCCUPYING"
        )
        room_order.end_date = datetime.now()
        room_order.status = "FINISHED"
        room_order.save()

        # make room available
        room = room_order.room
        if room != None:
            room.status = "AVAILABLE"
            room.save()

        serializer = HotelUserSerializer(hotel_user, many=False)

        return Response({'data': serializer.data})


class CheckoutDetailView(APIView):
    def get(self, request, username, format=None):
        hotel_user = getHotelUser(username)

        serializer = CheckoutListSerializer(hotel_user, many=False)

        return Response({'data': serializer.data})

# pages


class CheckoutPage(APIView):
    def get(self, request, format=None):
        if not request.user.is_authenticated:
            raise PermissionDenied(
                {"error_message": "You don't have permission to access"})

        hotel_user = getHotelUser(request.user)

        if hotel_user.role == 'GUEST':
            raise PermissionDenied(
                {"error_message": "You don't have permission to access"})

        return render(request, 'checkout/index.html')


class CheckoutDetailPage(APIView):
    def get(self, request, username, format=None):
        if not request.user.is_authenticated:
            raise PermissionDenied(
                {"error_message": "You don't have permission to access"})

        hotel_user = getHotelUser(request.user)

        if hotel_user.role == 'GUEST':
            raise PermissionDenied(
                {"error_message": "You don't have permission to access"})

        return render(request, 'checkout/detail/index.html')
