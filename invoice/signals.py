# invoice/signals.py
from django.db import transaction
from django.db.models import F
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Invoice
from store.models import Item
from django.core.exceptions import ValidationError

@receiver(post_save, sender=Invoice)
def invoice_post_save(sender, instance: Invoice, created, **kwargs):
    if not created:
        return
    with transaction.atomic():
        item = Item.objects.select_for_update().get(pk=instance.item_id)

        # Ensure enough stock (optional)
        if item.quantity < instance.quantity:
            # Option 1: raise to prevent invoice creation (you might want different behavior)
            raise ValidationError("Not enough stock for this invoice")
            # Option 2: set item.quantity = 0 and allow negative? (not recommended)

        item.quantity = F('quantity') - instance.quantity
        item.save()
