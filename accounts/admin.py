from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile
from django.urls import path
from django.template.response import TemplateResponse
from bookings.models import Booking
from resorts.models import Resort
from inventory.models import InventoryItem

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'phone', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2', 'role'),
        }),
    )



class ResortSathiAdminSite(admin.AdminSite):
    site_header = "Resort Sathi Admin"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_view(self.custom_index), name='index'),
        ]
        return custom_urls + urls

    def custom_index(self, request):
        total_bookings = Booking.objects.count()
        active_resorts = Resort.objects.filter(is_verified=True).count()
        low_stock = InventoryItem.objects.filter(quantity_in_stock__lte=models.F('reorder_level')).count()

        context = dict(
            self.each_context(request),
            total_bookings=total_bookings,
            active_resorts=active_resorts,
            low_stock=low_stock,
        )
        return TemplateResponse(request, "admin/index.html", context)

admin_site = ResortSathiAdminSite(name='resortsathi_admin')


