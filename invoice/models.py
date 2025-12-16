from django.db import models
from django_extensions.db.fields import AutoSlugField

from store.models import Item, Delivery
from accounts.models import Customer

class Invoice(models.Model):
    """
    Represents an invoice for a purchased item.

    Attributes:
        slug (str): Unique slug based on the date.
        date (datetime): Date of invoice creation.
        customer_name (str): Name of the customer.
        contact_number (str): Customer's contact number.
        item (ForeignKey): The invoiced item.
        price_per_item (float): Price per item.
        quantity (float): Number of items purchased.
        shipping (float): Shipping charges.
        total (float): Total before shipping.
        grand_total (float): Total including shipping.
    """

    slug = AutoSlugField(unique=True, populate_from='date')
    date = models.DateTimeField(
        auto_now=True,
        verbose_name='Date (e.g., 2022/11/22)'
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL, # Nếu xóa khách thì hóa đơn vẫn còn (nhưng mất tên)
        null=True,
        blank=True,
        related_name='invoices'
    )

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price_per_item = models.FloatField(verbose_name='Price Per Item (Ksh)')
    quantity = models.FloatField(default=0.00)
    shipping = models.FloatField(verbose_name='Shipping and Handling')
    total = models.FloatField(
        verbose_name='Total Amount (Ksh)', editable=False
    )
    grand_total = models.FloatField(
        verbose_name='Grand Total (Ksh)', editable=False
    )

    def save(self, *args, **kwargs):
        """
        Update total and grand_total before saving.
        """
        # Giữ lại logic tính toán
        self.total = round(self.quantity * self.price_per_item, 2)
        self.grand_total = round(self.total + self.shipping, 2)
        
        return super().save(*args, **kwargs)

    def __str__(self):
        # Lấy tên khách hàng an toàn
        if self.customer:
            cust_name = f"{self.customer.first_name} {self.customer.last_name}"
        else:
            cust_name = "Guest"
            
        # Trả về chuỗi định dạng chuẩn: "Invoice #ID - Tên khách"
        return f"#{self.id} - {cust_name}"
