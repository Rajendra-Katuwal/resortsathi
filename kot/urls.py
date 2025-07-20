from django.urls import path
from .views import *

urlpatterns = [
    # path('kot-items/', kot_items, name='kot_items'),
    path('create/', create_kot, name='create_kot'),
    path('', kot, name='kot_list'),
    
    # path('kot-items/delete/<int:pk>/', delete_kot_item, name='delete_kot_item'),
    # path("", kot_list, name="kot"),
    path("kot/delete/<int:pk>/", delete_kot, name="delete_kot"),
    path('menu-items/', menu_items, name='menu_items'),
    path('menu-items/delete/<int:pk>/', delete_menu_item, name='delete_menu_item'),
]