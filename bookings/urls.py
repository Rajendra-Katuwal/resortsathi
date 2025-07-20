from django.urls import path
from .views import *

urlpatterns = [
    path('', booking, name="booking"),
    path('booking/delete/<int:pk>/', delete_booking, name='delete_booking'),
]
