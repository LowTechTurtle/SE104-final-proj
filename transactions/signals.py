# transactions/signals.py
from decimal import Decimal
from django.db import transaction
from django.db.models import F
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Purchase
from bills.models import Bill
from store.models import Item
from django.conf import settings

@receiver(post_save, sender=Purchase)
def purchase_post_save(sender, instance: Purchase, created, **kwargs):
    if not created:
        return

    # Create bill and increment inventory atomically
    with transaction.atomic():
        # Lock the item row for update to avoid race conditions
        item = Item.objects.select_for_update().get(pk=instance.item_id)

        # increase stock by purchase.quantity
        item.quantity = F('quantity') + instance.quantity
        item.save()

        # refresh to get concrete int value if needed
        item.refresh_from_db()

        # Create associated bill
        Bill.objects.create(
            purchase=instance,
            payment_details=f"Purchase #{instance.pk}",
            status=False,
        )

# transactions/signals.py (add this function)
from .models import Sale, SaleDetail

@receiver(post_save, sender=Sale)
def sale_post_save(sender, instance: Sale, created, **kwargs):
    # Option A: If SaleDetails are created after Sale, you may instead listen to SaleDetail.post_save
    # Implementing on Sale to iterate pre-existing details:
    if not created:
        return
    with transaction.atomic():
        # lock all item rows involved
        detail_qs = instance.saledetail_set.select_related('item').all()
        item_ids = [d.item_id for d in detail_qs]
        items_map = {it.id: it for it in Item.objects.select_for_update().filter(id__in=item_ids)}

        for d in detail_qs:
            item = items_map[d.item_id]
            if item.quantity < d.quantity:
                raise ValidationError(f"Not enough stock for item {item.name}")
            item.quantity = F('quantity') - d.quantity
            item.save()
