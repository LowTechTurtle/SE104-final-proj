from django.contrib import admin
from .models import Bill


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'purchase', 'payment_details', 'status']

    def has_add_permission(self, request, obj=None):
        # No one can add via admin; creation only via signals
        return False