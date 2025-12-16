# Django core imports
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin
# Class-based views
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView
)

# Authentication and permissions
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Third-party packages
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin

# Local app imports
from .models import Bill
from .tables import BillTable
from accounts.models import Profile

import openpyxl
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

class BillListView(LoginRequiredMixin, ExportMixin, SingleTableView):
    """View for listing bills."""
    model = Bill
    table_class = BillTable
    template_name = 'bills/bill_list.html'
    context_object_name = 'bills'
    paginate_by = 10
    SingleTableView.table_pagination = False


class BillUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """View for updating an existing bill."""
    model = Bill
    template_name = 'bills/billupdate.html'
    fields = [
        'payment_details',
        'status'
    ]
    permission_required = "bills.change_bill"

    def test_func(self):
        """Check if the user has the required permissions."""
        return self.request.user.profile in Profile.objects.all()


class BillDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """View for deleting a bill."""
    model = Bill
    template_name = 'bills/billdelete.html'
    permission_required = "bills.delete_bill"

    def get_success_url(self):
        """Redirect to the list of bills after successful deletion."""
        return reverse('bill_list')

@login_required
def export_bills(request):
    """
    Export danh sách Hóa đơn nhập hàng (Bill)
    """
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Bills_Report.xlsx"'

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Bills"

    # 1. Định nghĩa Header
    columns = [
        'Bill ID', 
        'Vendor Name',    # Tên nhà cung cấp
        'Description',    # Mô tả đơn nhập
        'Contact Number', # SĐT nhà cung cấp
        'Email',          # Email nhà cung cấp
        'Payment Details',# Chi tiết thanh toán
        'Amount',         # Tổng tiền
        'Status',         # Trạng thái (Paid/Pending)
        'Order Date'      # Ngày nhập hàng
    ]
    ws.append(columns)

    # Format Header in đậm
    header_font = openpyxl.styles.Font(bold=True)
    for cell in ws[1]:
        cell.font = header_font

    # 2. Query dữ liệu
    # Dùng select_related để nối: Bill -> Purchase -> Vendor (Tối ưu tốc độ)
    rows = Bill.objects.all().select_related('purchase', 'purchase__vendor').order_by('-id')

    for bill in rows:
        # -- Lấy thông tin Purchase & Vendor (An toàn tuyệt đối) --
        purchase = bill.purchase
        vendor_name = "N/A"
        vendor_phone = "-"
        vendor_email = "-"
        description = "-"
        amount = 0
        order_date = "-"

        if purchase:
            description = purchase.description if purchase.description else "-"
            amount = purchase.total_value
            if purchase.order_date:
                order_date = purchase.order_date.strftime('%Y-%m-%d')
            
            # Lấy thông tin Vendor
            if purchase.vendor:
                vendor_name = purchase.vendor.name
                vendor_phone = purchase.vendor.phone if purchase.vendor.phone else "-"
                vendor_email = purchase.vendor.email if purchase.vendor.email else "-"

        # -- Xử lý trạng thái --
        status_text = "Paid" if bill.status else "Pending"

        # -- Ghi dòng dữ liệu --
        ws.append([
            bill.id,
            vendor_name,
            description,
            vendor_phone,
            vendor_email,
            bill.payment_details,
            amount,
            status_text,
            order_date
        ])

    # 3. Auto-fit độ rộng cột
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

    wb.save(response)
    return response