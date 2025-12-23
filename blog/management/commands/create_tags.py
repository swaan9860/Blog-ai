from django.core.management.base import BaseCommand
from blog.models import Tag

class Command(BaseCommand):
    help = 'Create predetermined tags'

    def handle(self, *args, **kwargs):
        tags = [
            'Travel', 'Technology', 'Health', 'Food', 'Lifestyle',
            'Packing Tips', 'Flying Tips', 'Booking Travel',  # Based on your existing code
            # Add more as needed
        ]
        for tag_name in tags:
            Tag.objects.get_or_create(name=tag_name)
        self.stdout.write(self.style.SUCCESS('Predetermined tags created!'))