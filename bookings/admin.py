# yourapp/admin.py
from django.contrib import admin
from django import forms
from .models import Booking
from accounts.widgets import NepaliDatePickerWidget


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass
