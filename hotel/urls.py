from django.urls import path
from .views import hotel_register,hotel_list

urlpatterns = [
    path('hotel_register',hotel_register, name='hotel_register'),
    path('hotel_list',hotel_list, name='hotel_list'),
]