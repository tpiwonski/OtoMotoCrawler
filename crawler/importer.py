from django.utils import timezone

from crawler.models import Offer


class Importer(object):
    """
    Import car offers into the database.
    """

    def __init__(self, crawler):
        self.crawler = crawler

    def import_car_offers(self, pages):
        fetched_offers = self.crawler.get_car_offers(pages)

        for offer in fetched_offers:
            o = Offer.objects.filter(offer_id=offer['offer_id'])
            
            if len(o):
                print("Offer {} already exists".format(offer['offer_id']))
                continue

            print("Adding offer {}".format(offer['offer_id']))

            o = Offer(offer_id=offer['offer_id'], offer_name=offer['offer_name'], offer_url=offer['offer_url'], 
                      offer_price=offer['offer_price'], car_brand=offer['car_brand'], car_model=offer['car_model'], 
                      dealer_phone=offer['dealer_phone'], dealer_name=offer['dealer_name'], import_date=timezone.now())

            o.save()
