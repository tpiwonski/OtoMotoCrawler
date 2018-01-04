from django.core.management.base import BaseCommand, CommandError

from crawler.models import Offer

class Command(BaseCommand):
    help = 'Delete all imported car offers'
    
    def handle(self, *args, **options):
        Offer.objects.all().delete()
