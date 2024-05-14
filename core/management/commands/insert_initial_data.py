from django.core.management import BaseCommand
from authentication.models import UserRole


class Command(BaseCommand):
    help = 'Inserts initial data into the databse'

    def handle(self, *args, **options):
        if not UserRole.objects.exists():
            UserRole.objects.create(name='Main Edition')
            UserRole.objects.create(name='Sub Edition')
