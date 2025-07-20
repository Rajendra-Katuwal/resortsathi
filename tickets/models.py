# tickets/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import uuid

User = get_user_model()

from django.db import models
import uuid

class TicketCounter(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class TicketTemplate(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    counter = models.ForeignKey(TicketCounter, on_delete=models.SET_NULL, null=True)
    template = models.ForeignKey(TicketTemplate, on_delete=models.SET_NULL, null=True)
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)

    # Only set if customer is a corporate or organization
    customer_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    customer_id = models.PositiveIntegerField(null=True, blank=True)
    customer = GenericForeignKey('customer_type', 'customer_id')

    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('online', 'Online'),
        ('credit', 'Credit'),
    ]
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    is_valid = models.BooleanField(default=True)

    class Meta:
        ordering = ['-issued_at']

    def is_walkin(self):
        return self.customer_type is None and self.customer_id is None

    def __str__(self):
        if self.is_walkin():
            return f"Walk-in Ticket #{self.ticket_id}"
        else:
            return f"{self.customer} - Ticket #{self.ticket_id}"
        
    @property
    def total_price(self):
        if self.template and self.quantity:
            return self.template.price * self.quantity
        return 0

    