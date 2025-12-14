from django.contrib import admin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Invoice model.
    """
    # Thay thế 2 trường nhập tay cũ bằng trường 'customer' chọn từ danh sách
    fields = (
        'customer', 'item',
        'price_per_item', 'quantity', 'shipping'
    )
    
    # Hiển thị cột Customer và SĐT (lấy từ bảng Customer sang)
    list_display = (
        'date', 'customer', 'get_contact_number', 'item',
        'price_per_item', 'quantity', 'shipping', 'total',
        'grand_total'
    )

    # Thêm thanh tìm kiếm để tìm theo tên khách hoặc tên hàng hóa
    search_fields = ('customer__first_name', 'customer__last_name', 'customer__phone', 'item__name')

    # Hàm phụ giúp lấy SĐT từ bảng Customer để hiển thị lên list
    def get_contact_number(self, obj):
        # Nếu invoice có gắn khách hàng thì trả về sđt, không thì trả về '-'
        return obj.customer.phone if obj.customer else '-'
    
    # Đặt tên cho cột hiển thị là "Contact Number"
    get_contact_number.short_description = 'Contact Number'