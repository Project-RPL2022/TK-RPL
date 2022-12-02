from django.urls import path
from .views import book_room,create_room, list_room
urlpatterns = [
    path('book_room/<str:hotel_name>',book_room,name='book_room'),
    path('create_room/<str:hotel_name>',create_room,name='create_room'),
    path('list_room/<str:hotel_name>',list_room,name='list_room')
]