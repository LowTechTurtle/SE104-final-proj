"""
Module: admin.py

Django admin configurations for managing categories, items, and deliveries.

This module defines the following admin classes:
- CategoryAdmin: Configuration for the Category model in the admin interface.
- ItemAdmin: Configuration for the Item model in the admin interface.
- DeliveryAdmin: Configuration for the Delivery model in the admin interface.
"""

from django.contrib import admin
from .models import Category, Item, Delivery


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.
    """
    list_display = ('name', 'slug')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Item model.
    """
    list_display = (
        'name', 'category', 'quantity', 'price', 'vendor'
    )
    search_fields = ('name', 'category__name', 'vendor__name')
    list_filter = ('category', 'vendor')
    ordering = ('name',)

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['id', 'location', 'is_delivered']
    ordering = ['id']   # remove 'date'
    list_filter = ['is_delivered']

    def has_add_permission(self, request, obj=None):
        return False