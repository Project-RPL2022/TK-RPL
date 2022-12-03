from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from accounts.models import HotelUser
from room.models import Room, RoomOrder, RoomPayment
from roomservice.models import RoomService, RoomServiceOrder, RoomServicePayment
from main.utils import getHotelUser
from tkrpl.auth import get_role
import requests
from requests.exceptions import ConnectionError

# Create your views here.
@login_required
def user_is_guest(request):
    if not request.user.is_authenticated:
        return {
            "success": False,
            "message": "User is not authenticated",
        }
    if get_role(request) != 'GUEST':
        return {
            "success": False,
            "message": "User role is not GUEST",
        }
    return {
            "success": True
        }
    

@login_required
def pay_room_payment(request, room_payment_id):
    # Check if user is guest
    is_guest = user_is_guest(request)
    if not is_guest.get("success"):
        return JsonResponse(is_guest)
    # Check if room order and room payment available and is associated with this user
    hotel_user = getHotelUser(request.user)
    try:
        room_payment = RoomPayment.objects.get(pk=room_payment_id)
    except RoomPayment.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "RoomPayment with id " + str(room_payment_id) + " does not exist",
            })
    room_order = room_payment.room_order
    if hotel_user != room_order.guest:
        return JsonResponse({
            "success": False,
            "message": "User is not associated with this payment",
            })
    if room_payment.status != "WAITING":
        return JsonResponse({
            "success": False,
            "message": "This RoomPayment is already paid",
            })
    
    # Connect to payment service, and paying according to price amount
    payload = {'price': room_payment.price}
    try:
        r = requests.post('https://dummy-wallet-api.fly.dev/pay', data=payload)
    except ConnectionError as e:
        return JsonResponse({
            "success": False,
            "message": "Can't connect to payment service"
        })
    r_dict = r.json()
    if r_dict.get('success'):
        room_payment.status = "UNVERIFIED"
        room_payment.save()
    return JsonResponse(r_dict)


@login_required
def pay_room_service_payment(request, room_service_payment_id):
    # Check if user is guest
    is_guest = user_is_guest(request)
    if not is_guest.get("success"):
        return JsonResponse(is_guest)
    # Check if room service order and room service payment available and is associated with this user
    hotel_user = getHotelUser(request.user)
    try:
        room_service_payment = RoomServicePayment.objects.get(pk=room_service_payment_id)
    except RoomServicePayment.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "RoomServicePayment with id " + str(room_service_payment_id) + " does not exist",
            })
    room_service_order = room_service_payment.room_service_order
    if hotel_user != room_service_order.guest:
        return JsonResponse({
            "success": False,
            "message": "User is not associated with this payment",
            })
    if room_service_payment.status != "WAITING":
        return JsonResponse({
            "success": False,
            "message": "This RoomPayment is already paid",
            })
    
    # Connect to payment service, and paying according to price amount
    payload = {'price': room_service_payment.amount}
    try:
        r = requests.post('https://dummy-wallet-api.fly.dev/pay', data=payload)
    except ConnectionError as e:
        return JsonResponse({
            "success": False,
            "message": "Can't connect to payment service"
        })
    r_dict = r.json()
    if r_dict.get('success'):
        room_service_payment.status = "UNVERIFIED"
        room_service_payment.save()
    return JsonResponse(r_dict)