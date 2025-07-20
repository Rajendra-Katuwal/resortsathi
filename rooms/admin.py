from django.contrib import admin
from .models import RoomType, Room

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'resort', 'room_type', 'price_per_night', 'max_guests', 'is_available', 'created_at')
    list_filter = ('is_available', 'room_type', 'resort')
    search_fields = ('name', 'resort__name')
