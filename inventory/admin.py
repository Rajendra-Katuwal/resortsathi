from django.contrib import admin
from .models import Ingredient, InventoryItem, InventoryTransaction

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'quantity_in_stock', 'reorder_level')

@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ('inventory_item', 'quantity_change', 'transaction_type', 'date')
