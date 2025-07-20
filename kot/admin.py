from django.contrib import admin
from .models import MenuItem, KOT, KOTItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('name',)

@admin.register(KOT)
class KOTAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('booking__id',)

@admin.register(KOTItem)
class KOTItemAdmin(admin.ModelAdmin):
    list_display = ('kot', 'menu_item', 'quantity')
    search_fields = ('menu_item__name',)
