from django.urls import path
from .views import *

urlpatterns = [
    path('room-type/', room_type, name='room_type'),
    path('room-type/delete/<int:pk>/', delete_room_type, name='delete_room_type'),
    path('', room, name='room'),
    path('room/delete/<int:pk>/', delete_room, name='delete_room'),
]