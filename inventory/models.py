from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=150)
    unit = models.CharField(max_length=50)  # e.g. kg, liter, pcs

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    ingredient = models.OneToOneField(Ingredient, on_delete=models.CASCADE)
    quantity_in_stock = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_level = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.ingredient.name

    def is_below_reorder(self):
        return self.quantity_in_stock <= self.reorder_level

class InventoryTransaction(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity_change = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type_choices = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjustment', 'Adjustment'),
    ]
    transaction_type = models.CharField(max_length=10, choices=transaction_type_choices)
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.transaction_type} {self.quantity_change} of {self.inventory_item}"

class Recipe(models.Model):
    menu_item = models.ForeignKey('kot.MenuItem', on_delete=models.CASCADE, related_name='recipes')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)  # quantity needed per 1 menu item unit

    def __str__(self):
        return f"{self.ingredient.name} for {self.menu_item.name}"
