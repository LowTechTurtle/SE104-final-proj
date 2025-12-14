import csv

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = "Create Manager and Staff groups based on a use-case CSV file"

    MODEL_KEYWORDS = {
        "customer": ("accounts", "customer"),
        "vendor": ("accounts", "vendor"),
        "profile": ("accounts", "profile"),
        "staff": ("auth", "user"),
        "manager": ("auth", "user"),
        "user": ("auth", "user"),
        "group": ("auth", "group"),
        "permission": ("auth", "permission"),
        "bill": ("bills", "bill"),
        "invoice": ("invoice", "invoice"),
        "purchase": ("transactions", "purchase"),
        "sale detail": ("transactions", "saledetail"),
        "sale": ("transactions", "sale"),
        "item": ("store", "item"),
        "category": ("store", "category"),
        "delivery": ("store", "delivery"),
    }

    ACTION_KEYWORDS = {
        "create": "add",
        "add": "add",
        "update": "change",
        "edit": "change",
        "change": "change",
        "delete": "delete",
        "remove": "delete",
        "view": "view",
        "list": "view",
        "see": "view",
    }

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_path",
            type=str,
            help="Path to usecase CSV file",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what permissions would be applied without changing the database",
        )

    def handle(self, *args, **options):
        csv_path = options["csv_path"]
        dry_run = options["dry_run"]

        try:
            f = open(csv_path, newline="", encoding="utf-8")
        except FileNotFoundError:
            raise CommandError(f"CSV file not found: {csv_path}")

        reader = csv.DictReader(f)

        manager_group, _ = Group.objects.get_or_create(name="Manager")
        staff_group, _ = Group.objects.get_or_create(name="Staff")

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY-RUN MODE ENABLED"))
        else:
            manager_group.permissions.clear()
            staff_group.permissions.clear()
            self.stdout.write("Cleared existing permissions for Manager and Staff")

        for row in reader:
            usecase_name = row.get("Use Case Name", "").lower()
            description = row.get("Description", "").lower()
            actors = row.get("Actors", "").lower()

            text = f"{usecase_name} {description}"

            action = self._detect_action(text)
            model_info = self._detect_model(text)

            if not action or not model_info:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping: cannot infer permission for '{row.get('Use Case Name')}'"
                    )
                )
                continue

            app_label, model_name = model_info
            codename = f"{action}_{model_name}"

            try:
                content_type = ContentType.objects.get(
                    app_label=app_label, model=model_name
                )
                permission = Permission.objects.get(
                    content_type=content_type, codename=codename
                )
            except (ContentType.DoesNotExist, Permission.DoesNotExist):
                self.stdout.write(
                    self.style.WARNING(f"Permission not found: {codename}")
                )
                continue

            if "manager" in actors:
                if dry_run:
                    self.stdout.write(
                        f"[DRY-RUN] Manager → {permission.codename}"
                    )
                else:
                    manager_group.permissions.add(permission)

            if "staff" in actors:
                if dry_run:
                    self.stdout.write(
                        f"[DRY-RUN] Staff → {permission.codename}"
                    )
                else:
                    staff_group.permissions.add(permission)

        if dry_run:
            self.stdout.write(
                self.style.SUCCESS("Dry-run completed. No database changes were made.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("Group setup completed successfully.")
            )

    def _detect_action(self, text):
        for key, action in self.ACTION_KEYWORDS.items():
            if key in text:
                return action
        return None

    def _detect_model(self, text):
        for key, model in self.MODEL_KEYWORDS.items():
            if key in text:
                return model
        return None

