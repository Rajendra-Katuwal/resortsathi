from django.contrib import admin
from .models import Resort

@admin.register(Resort)
class ResortAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city', 'state', 'country', 'contact_email', 'contact_phone', 'is_verified', 'created_at')
    search_fields = ('name', 'city', 'state', 'country')
    list_filter = ('city', 'state', 'country', 'is_verified')
