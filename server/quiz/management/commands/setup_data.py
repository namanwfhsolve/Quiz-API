from django.core.management import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.create_superuser()

    def create_superuser(self):
        u = User.objects.create_superuser("admin", "admin@gmail.com", "password")
        self.stdout.write(f"created user {u}")
