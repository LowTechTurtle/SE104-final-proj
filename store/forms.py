from django import forms
from .models import Item, Category, Delivery

from transactions.models import Sale
from invoice.models import Invoice # <--- 1. Import Invoice

class ItemForm(forms.ModelForm):
    """
    A form for creating or updating an Item in the inventory.
    """
    class Meta:
        model = Item
        fields = [
            'name',
            'description',
            'category',
            'quantity',
            'price',
            'vendor'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2
                }
            ),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01'
                }
            ),
            'vendor': forms.Select(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    """
    A form for creating or updating category.
    """
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name',
                'aria-label': 'Category Name'
            }),
        }
        labels = {
            'name': 'Category Name',
        }


class DeliveryForm(forms.ModelForm):
    # Chỉ còn lại dropdown Invoice
    invoice = forms.ModelChoiceField(
        queryset=Invoice.objects.all().order_by('-id'),
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'style': 'width: 100%;'
        }),
        label="Select Invoice",
        required=True # Bắt buộc phải chọn
    )

    class Meta:
        model = Delivery
        fields = ['invoice', 'location', 'is_delivered'] # Bỏ sale ra khỏi list
        
        widgets = {
            'location': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Leave empty to use Customer Address'
            }),
            'is_delivered': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'width: 20px; height: 20px;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(DeliveryForm, self).__init__(*args, **kwargs)
        
        # Nếu đang Update: Khóa trường Invoice lại không cho đổi
        if self.instance.pk:
            self.fields['invoice'].disabled = True
            self.fields['invoice'].widget.attrs['readonly'] = True
            self.fields['invoice'].widget.attrs['class'] += ' bg-light'