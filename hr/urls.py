from django.urls import path
from hr import views

urlpatterns = [
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/save/', views.save_employee, name='save_employee'),
    path('employees/delete/<int:emp_id>/', views.delete_employee, name='delete_employee'),
    path('departments/', views.department_list, name='department_list'),
    path('departments/delete/<int:pk>/', views.delete_department, name='delete_department'),
    path('positions/', views.position_list, name='position_list'),
    path('positions/delete/<int:id>/', views.delete_position, name='delete_position'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/delete/<int:id>/', views.delete_attendance, name='delete_attendance'),
    path('payslips/', views.payslip_list, name='payslip_list'),
    path('payslips/save/', views.save_payslip, name='save_payslip'),
    path('payslips/delete/<int:pk>/', views.delete_payslip, name='delete_payslip'),
]
