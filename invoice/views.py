# Django core imports
from django.urls import reverse

# Authentication and permissions
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Class-based views
from django.views.generic import (
    DetailView, CreateView, UpdateView, DeleteView
)

# Third-party packages
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin

# Local app imports
from .models import Invoice
from .tables import InvoiceTable
# --- QUAN TRỌNG: Import Form vừa tạo ---
from .forms import InvoiceForm  

from store.models import Delivery

class InvoiceListView(LoginRequiredMixin, ExportMixin, SingleTableView):
    """
    View for listing invoices with table export functionality.
    """
    model = Invoice
    table_class = InvoiceTable
    template_name = 'invoice/invoicelist.html'
    context_object_name = 'invoices'
    paginate_by = 10
    table_pagination = False


class InvoiceDetailView(DetailView):
    """
    View for displaying invoice details.
    """
    model = Invoice
    template_name = 'invoice/invoicedetail.html'

    def get_success_url(self):
        return reverse('invoice-detail', kwargs={'slug': self.object.pk})


class InvoiceCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new invoice.
    """
    model = Invoice
    template_name = 'invoice/invoicecreate.html'
    
    # --- ĐOẠN ĐÃ SỬA ---
    # Bỏ fields = [...] vì nó chứa trường cũ và không dùng widget Select2
    # Thay bằng form_class để dùng form xịn trong forms.py
    form_class = InvoiceForm
    # -------------------

    def get_success_url(self):
        return reverse('invoicelist')

    # --- THÊM HÀM NÀY ĐỂ TỰ ĐỘNG TẠO DELIVERY ---
    def form_valid(self, form):
        # 1. Lưu Invoice trước
        response = super().form_valid(form)
        
        # 2. Lấy object Invoice vừa tạo ra
        created_invoice = self.object
        
        # 3. Tự động tạo một Delivery gắn với Invoice này
        Delivery.objects.create(
            invoice=created_invoice,
            # Lấy địa chỉ khách hàng làm địa chỉ giao hàng mặc định
            location=created_invoice.customer.address if created_invoice.customer else "Tại cửa hàng",
            is_delivered=False # Mặc định là chưa giao
        )
        
        return response
    



class InvoiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating an existing invoice.
    """
    model = Invoice
    template_name = 'invoice/invoiceupdate.html'
    
    # --- ĐOẠN ĐÃ SỬA ---
    # Tương tự CreateView, ta dùng form_class
    form_class = InvoiceForm
    # -------------------

    def get_success_url(self):
        return reverse('invoicelist')

    def test_func(self):
        return self.request.user.is_superuser


class InvoiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleting an invoice.
    """
    model = Invoice
    template_name = 'invoice/invoicedelete.html'
    success_url = '/products'

    def get_success_url(self):
        return reverse('invoicelist')

    def test_func(self):
        return self.request.user.is_superuser