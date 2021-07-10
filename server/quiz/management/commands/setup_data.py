from django.core.management import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.create_superuser()

    def create_superuser(self):
        u = User.objects.create_superuser("namantam1", "namantam1@gmail.com", "naman")
        self.stdout.write(f"created user {u}")
