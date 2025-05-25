from django.core.management.base import BaseCommand
from django.utils import timezone
from ...models import TemporaryFile

class Command(BaseCommand):
    help = 'Clean up expired temporary files'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_files = TemporaryFile.objects.filter(expires_at__lt=now)
        count = expired_files.count()
        expired_files.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} expired temporary files'))
