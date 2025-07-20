from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('', views.ticket_list_view, name='ticket-list'),
    path('issue/', views.issue_ticket, name='issue-ticket'),
    path('delete/<int:pk>/', views.delete_ticket, name='delete-ticket'),
    path('print/<int:pk>/', views.print_ticket_view, name='print-ticket'),

    # Ticket Counter
    path('counters/', views.counter_list_view, name='counter-list'),
    path('counters/edit/<int:pk>/', views.counter_create_or_edit, name='counter-edit'),
    path('counters/create/', views.counter_create_or_edit, name='counter-create'),
    path('counters/delete/<int:pk>/', views.counter_delete, name='counter-delete'),

    # Ticket Template
    path('templates/', views.template_list_view, name='template-list'),
    path('templates/edit/<int:pk>/', views.template_create_or_edit, name='template-edit'),
    path('templates/create/', views.template_create_or_edit, name='template-create'),
    path('templates/delete/<int:pk>/', views.template_delete, name='template-delete'),
    path('print/<int:pk>/', views.print_ticket_view, name='print-ticket'),
]
