from django.urls import path
from .views import *

urlpatterns = [
    path('ingredients/', ingredient, name='ingredients'),
    path('ingredient/delete/<int:pk>/', delete_ingredient, name='delete_ingredient'),
    path('', inventory, name='inventory_items'),
    path('inventory/delete/<int:pk>/', delete_inventory, name='delete_inventory'),
    path('inventory-transactions/', inventory_transactions, name='inventory_trans'),
    path('inventory-transactions/delete/<int:pk>/', delete_inventory_transaction, name='delete_inventory_transaction'),
]