# Django core imports
from django.urls import path
from . import views
# Local app imports
from .views import (
    BillListView,
    BillUpdateView,
    BillDeleteView
)

# URL patterns
urlpatterns = [
    # Bill URLs
    path(
        'bills/',
        BillListView.as_view(),
        name='bill_list'
    ),
    path(
        'bill/<slug:slug>/update/',
        BillUpdateView.as_view(),
        name='bill_update'
    ),
    path(
        'bill/<int:pk>/delete/',
        BillDeleteView.as_view(),
        name='bill_delete'
    ),
    path('export-bills/', 
        views.export_bills, 
        name='export_bills'),
]
