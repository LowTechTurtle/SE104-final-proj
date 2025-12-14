from django import forms
from .models import Invoice
from accounts.models import Customer
from store.models import Item

class InvoiceForm(forms.ModelForm):
    # Tạo ô chọn khách hàng có tìm kiếm
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 
            'style': 'width: 100%;'
        }),
        label="Customer"
    )

    class Meta:
        model = Invoice
        # Các trường cần hiển thị trong form
        fields = ['customer', 'item', 'price_per_item', 'quantity', 'shipping']
        
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control select2'}), # Tìm kiếm sản phẩm
            'price_per_item': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
            'shipping': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Shipping Cost'}),
        }