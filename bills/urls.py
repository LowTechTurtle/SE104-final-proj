# Django core imports
from django.urls import path

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
]
