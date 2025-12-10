from django.contrib import admin
from .models import Sale, SaleDetail, Purchase


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Sale model.
    """
    list_display = (
        'id',
        'customer',
        'date_added',
        'grand_total',
        'amount_paid',
        'amount_change'
    )
    search_fields = ('customer__name', 'id')
    list_filter = ('date_added', 'customer')
    ordering = ('-date_added',)
    readonly_fields = ('date_added',)
    date_hierarchy = 'date_added'

    def save_model(self, request, obj, form, change):
        """
        Save the Sale instance, overriding the default save behavior.
        """
        super().save_model(request, obj, form, change)


@admin.register(SaleDetail)
class SaleDetailAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the SaleDetail model.
    """
    list_display = (
        'id',
        'sale',
        'item',
        'price',
        'quantity',
        'total_detail'
    )
    search_fields = ('sale__id', 'item__name')
    list_filter = ('sale', 'item')
    ordering = ('sale', 'item')

    def save_model(self, request, obj, form, change):
        """
        Save the SaleDetail instance, overriding the default save behavior.
        """
        super().save_model(request, obj, form, change)

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'item', 'order_date', 'delivery_status']
    list_filter = ['delivery_status']
