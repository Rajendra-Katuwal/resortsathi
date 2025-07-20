from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import KOTItem
from inventory.models import InventoryTransaction, InventoryItem, Recipe

@receiver(post_save, sender=KOTItem)
def deduct_inventory_on_kotitem_create(sender, instance, created, **kwargs):
    if created:
        menu_item = instance.menu_item
        quantity_ordered = instance.quantity
        
        # Get related recipe ingredients
        recipes = Recipe.objects.filter(menu_item=menu_item)
        for recipe in recipes:
            try:
                inventory_item = InventoryItem.objects.get(ingredient=recipe.ingredient)
            except InventoryItem.DoesNotExist:
                continue  # Or log missing inventory item
                
            quantity_to_deduct = recipe.quantity * quantity_ordered
            
            # Deduct stock
            inventory_item.quantity_in_stock -= quantity_to_deduct
            inventory_item.save()
            
            # Record transaction
            InventoryTransaction.objects.create(
                inventory_item=inventory_item,
                quantity_change=-quantity_to_deduct,
                transaction_type='out',
                notes=f'Deducted for KOTItem #{instance.id} ({menu_item.name})'
            )
