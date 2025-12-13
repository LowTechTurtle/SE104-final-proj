from django import forms
from .models import Item, Category, Delivery

from transactions.models import Sale

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
    # Tạo dropdown chọn đơn hàng (Sale)
    sale = forms.ModelChoiceField(
        queryset=Sale.objects.all().order_by('-id'), # Đơn mới nhất lên đầu
        widget=forms.Select(attrs={
            'class': 'form-control select2', # Thêm class select2 để tí nữa dùng JS
            'style': 'width: 100%;'
        }),
        label="Select Sale Order"
    )

    class Meta:
        model = Delivery
        # Chỉ lấy 3 trường cần thiết
        fields = ['sale', 'location', 'is_delivered']
        
        widgets = {
            'location': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Leave empty to use Customer Address' # Gợi ý người dùng
            }),
            'is_delivered': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'width: 20px; height: 20px;' # Cho nút check to ra tí cho dễ bấm
            }),
        }