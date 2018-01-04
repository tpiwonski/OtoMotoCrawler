from django.utils import timezone

from .models import Offer


class Monitor(object):
    """
    Monitor imported car offers. Notify when an offer is sold.
    """
    
    def __init__(self, crawler, notifier):
        self.crawler = crawler
        self.notifier = notifier
    
    def monitor_offers(self):
        offers = Offer.objects.filter(sold=False)
        for offer in offers:
            exists = self.crawler.offer_exists(offer.offer_id)
            if not exists:
                print("Offer {} sold".format(offer.offer_id))

                offer.sell_date = timezone.now()
                offer.sold = True
                offer.save()

                self.notifier.offer_sold(offer)
            else:
                print("Offer {} still exists".format(offer.offer_id))
