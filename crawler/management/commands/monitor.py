from django.core.management.base import BaseCommand, CommandError

from crawler.scraper import Crawler, Parser
from crawler.monitor import Monitor
from crawler.notifier import SMSNotifier


class Command(BaseCommand):
    help = 'Monitor imported car offers'
    
    def handle(self, *args, **options):
        parser = Parser()
        crawler = Crawler(parser)
        notifier = SMSNotifier()
        monitor = Monitor(crawler, notifier)
        monitor.monitor_offers()
