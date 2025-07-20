# accounting/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Invoice
from django.utils.crypto import get_random_string

@receiver(pre_save, sender=Invoice)
def generate_invoice_number(sender, instance, **kwargs):
    if not instance.number:
        prefix = "INV"
        date_part = instance.issue_date.strftime("%Y%m%d") if instance.issue_date else "00000000"
        random_part = get_random_string(5).upper()
        instance.number = f"{prefix}-{date_part}-{random_part}"
