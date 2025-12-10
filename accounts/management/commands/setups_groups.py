# accounts/management/commands/setup_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.apps import apps

class Command(BaseCommand):
    help = "Create Manager and Staff groups with appropriate permissions"

    def handle(self, *args, **options):
        manager, _ = Group.objects.get_or_create(name='Manager')
        staff, _ = Group.objects.get_or_create(name='Staff')

        # example: allow staff to add sales & view items, but not delete
        perms = []
        perms += list(Permission.objects.filter(content_type__app_label='transactions', codename__in=['add_sale','view_sale','add_saledetail','view_saledetail']))
        perms += list(Permission.objects.filter(content_type__app_label='store', codename__in=['view_item']))
        perms += list(Permission.objects.filter(content_type__app_label='invoice', codename__in=['add_invoice','view_invoice']))
        # manager gets more
        manager_perms = perms + list(Permission.objects.filter(content_type__app_label='store', codename__in=['add_item','change_item'])) + list(Permission.objects.filter(content_type__app_label='accounts', codename__in=['change_vendor','add_vendor']))
        manager.permissions.set(manager_perms)
        staff.permissions.set(perms)
        self.stdout.write(self.style.SUCCESS("Groups created and permissions assigned"))

