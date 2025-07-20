from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    path('', views.customer_list, name='customer_list'),

    path('corporate/add/', views.corporate_customer_form, name='corporate_add'),
    path('corporate/edit/<int:pk>/', views.corporate_customer_form, name='corporate_edit'),

    path('ordinary/add/', views.ordinary_customer_form, name='ordinary_add'),
    path('ordinary/edit/<int:pk>/', views.ordinary_customer_form, name='ordinary_edit'),

    path('organization/add/', views.organization_customer_form, name='organization_add'),
    path('organization/edit/<int:pk>/', views.organization_customer_form, name='organization_edit'),

    path('delete/<str:customer_type>/<int:pk>/', views.delete_customer, name='customer_delete'),
]

