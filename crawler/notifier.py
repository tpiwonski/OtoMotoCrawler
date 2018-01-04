
class SMSNotifier(object):
    """
    Send SMS notifications.
    """

    def offer_sold(self, offer):
        print("Sending congratulation SMS to number {0} on selling {1}".format(offer.dealer_phone, offer.offer_id))
