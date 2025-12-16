from django.db import models
from autoslug import AutoSlugField
from transactions.models import Purchase

class Bill(models.Model):
    """Model representing a bill with various details and payment status."""

    slug = AutoSlugField(unique=True, populate_from='purchase')
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    payment_details = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        help_text='Details of the payment'
    )
    status = models.BooleanField(
        default=False,
        verbose_name='Paid',
        help_text='Payment status of the bill'
    )

    def __str__(self):
        # Lấy tên Vendor thông qua Purchase
        if self.purchase and self.purchase.vendor:
            return f"Bill from {self.purchase.vendor.name} (#{self.id})"
        return f"Bill #{self.id}"
