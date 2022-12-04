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


def user_is_admin(request):
    if not request.user.is_authenticated:
        return {
            "success": False,
            "message": "User is not authenticated",
        }
    if get_role(request) != 'HOTEL_ADMINISTRATOR':
        return {
            "success": False,
            "message": "User role is not HOTEL_ADMINISTRATOR",
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


def get_payment_info(request):
    if request.method != "POST":
        is_admin = user_is_admin(request)
        if not is_admin.get("success"):
            return JsonResponse(is_admin)
        payments = {
            "room-verifying": RoomPayment.objects.filter(status="UNVERIFIED"), 
            "room-verified": RoomPayment.objects.filter(status="VERIFIED"),
            "service-verifying": RoomPayment.objects.filter(status="UNVERIFIED"),
            "service-verified": RoomPayment.objects.filter(status="VERIFIED")
        }
        return render(request, 'payment/verification.html', payments)


@login_required
def room_payment_verify(request, room_payment_id):
    # Check if user is an admin
    is_admin = user_is_admin(request)
    if not is_admin.get("success"):
        return JsonResponse(is_admin)
    try:
        room_payment = RoomPayment.objects.get(pk=room_payment_id)
    except RoomPayment.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "RoomPayment with id " + str(room_payment_id) + " does not exist",
            })
    try:
        room_payment.status = "VERIFIED"
        room_payment.room_order.room.status = "OCCUPIED"
        room_payment.save()
    except:
        return JsonResponse({
            "success": False,
            "message": "RoomPayment status update " + str(room_payment_id) + " failed",
            })
    finally:
        return redirect(reverse_lazy("payment-verification"))


@login_required
def room_service_payment_verify(request, room_service_payment_id):
    # Check if user is an admin
    is_admin = user_is_admin(request)
    if not is_admin.get("success"):
        return JsonResponse(is_admin)
    # Getting the afiliated payment object to change the status
    try:
        room_service_payment = RoomServicePayment.objects.get(pk=room_service_payment_id)
    except RoomServicePayment.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "RoomServicePayment with id " + str(room_service_payment_id) + " does not exist",
            })
    try:
        room_service_payment.status = "VERIFIED"
        room_service_payment.room_service_order.status = "PROCESSED"
        room_service_payment.save()
    except:
        return JsonResponse({
            "success": False,
            "message": "RoomServicePayment status update " + str(room_service_payment_id) + " failed",
            })
    finally:
        return redirect(reverse_lazy("payment-verification"))


@login_required
def room_service_payment_reject(request, room_service_payment_id):
    # Check if user is an admin
    is_admin = user_is_admin(request)
    if not is_admin.get("success"):
        return JsonResponse(is_admin)
    # Getting the afiliated payment object to change the status
    try:
        room_service_payment = RoomServicePayment.objects.get(pk=room_service_payment_id)
    except RoomServicePayment.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "RoomServicePayment with id " + str(room_service_payment_id) + " does not exist",
            })
    try:
        room_service_payment.room_service_order.status = "REJECTED"
        room_service_payment.save()
    except:
        return JsonResponse({
            "success": False,
            "message": "RoomServicePayment status update " + str(room_service_payment_id) + " failed",
            })
    finally:
        return redirect(reverse_lazy("payment-verification"))