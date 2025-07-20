from django.contrib import admin
from .models import Employee, Department, Position, Attendance, LeaveRequest
# Register your models here.

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'resort', 'department', 'position', 'date_joined', 'is_active', 'salary')
    search_fields = ('user__first_name', 'user__last_name', 'department__name', 'position__title')
    list_filter = ('resort', 'department', 'position', 'is_active')