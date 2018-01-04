from django.core.management.base import BaseCommand, CommandError

from crawler.scraper import Crawler, Parser
from crawler.importer import Importer


class Command(BaseCommand):
    help = 'Import car offers'

    def add_arguments(self, parser):
        parser.add_argument('pages', type=int, help='Number of pages to import')

    def handle(self, *args, **options):
        pages = options['pages']

        self.stdout.write("Importing {} pages".format(pages))

        parser = Parser()
        crawler = Crawler(parser)
        importer = Importer(crawler)
        importer.import_car_offers(pages)
