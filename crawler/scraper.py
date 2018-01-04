import requests
from lxml import html
import json
import random


class Crawler(object):
    """
    A crawler for OTOMOTO site.
    """
    offers_url = "https://www.otomoto.pl/osobowe/poznan/?search%5Bbrand_program_id%5D%5B0%5D=&search%5Bdist%5D=50&search%5Bcountry%5D=&page={}"
    phone_url = "https://www.otomoto.pl/ajax/poznan/misc/contact/multi_phone/{}/0/"
    search_offer_url = "https://www.otomoto.pl/osobowe/q-{}/?search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D="

    def __init__(self, parser):
        self.session = requests.Session()
        self.parser = parser

    def get_car_offers(self, pages):
        results = []
        for page in range(1, pages + 1):
            url = self.offers_url.format(page)
            response = self.session.get(url)
            offers = self.parser.parse_car_offers(response.content)
            for offer in offers:
                details = self._get_offer_details(offer)
                offer.update(details)

            results.extend(offers)

        return results

    def _get_offer_details(self, offer):
        url = self.phone_url.format(offer['dealer_phone_code'])
        response = self.session.get(url)
        dealer_phone = self.parser.parse_phone_number(response.text)

        response = self.session.get(offer['offer_url'])
        offer = self.parser.parse_car_offer(response.content)
        offer['dealer_phone'] = dealer_phone

        return offer
    
    def offer_exists(self, offer_id):
        # mock that an offer was sold and is no longer available
        r = random.randint(1, 100)
        return False if r < 10 else True

        # url = self.search_offer_url.format(offer_id)
        # response = self.session.get(url)
        # results = self.parser.empty_search_results(response.content)
        # return not results['empty']


class Parser(object):
    """
    A parser for OTOMOTO pages.
    """

    def parse_car_offers(self, content):
        tree = html.fromstring(content)
        offers = []
        items = tree.xpath('//article[contains(@class, "offer-item")]')
        for item in items:
            info = item.xpath('.//a[contains(@class, "offer-title__link")]')[0]
            offer_url = info.attrib['href']
            offer_id = info.attrib['data-ad-id']
            offer_name = info.text.strip()

            price = item.xpath('.//span[contains(@class, "offer-price__number")]')[0]
            offer_price = int(price.text.replace(' ', ''))

            phone = item.xpath('.//div[@class="seller-phones"]/div[@class="number-box"]'
                               '/span[contains(@class, "spoiler")]')[0]
            phone_code = phone.attrib['data-id']

            offer = dict(offer_id=offer_id, offer_name=offer_name, offer_url=offer_url, offer_price=offer_price, 
                         dealer_phone_code=phone_code)
            offers.append(offer)

        return offers
    
    def parse_phone_number(self, content):
        result = json.loads(content)
        return result['value']

    def parse_car_offer(self, content):
        tree = html.fromstring(content)
        r = tree.xpath('//div[contains(@class, "offer-content__main-column")]'
                       '//div[contains(@class, "seller-box__seller-info")]'
                       '//h2[contains(@class, "seller-box__seller-name")]/descendant-or-self::*/text()')
        dealer_name = ''.join([c.strip() for c in r])

        r = tree.xpath('//div[contains(@class, "offer-params")]'
                       '//li[contains(@class, "offer-params__item") and '
                       './/span[@class="offer-params__label" and text()="Marka"]]')[0]
        car_brand = r.xpath('.//div[@class="offer-params__value"]/a')[0].text.strip()

        r = tree.xpath('//div[contains(@class, "offer-params")]'
                       '//li[contains(@class, "offer-params__item") and '
                       './/span[@class="offer-params__label" and text()="Model"]]')[0]
        car_model = r.xpath('.//div[@class="offer-params__value"]/a')[0].text.strip()

        return dict(dealer_name=dealer_name, car_brand=car_brand, car_model=car_model)

    def parse_search_results(self, content):
        tree = html.fromstring(content)
        r = tree.xpath('//div[@class="om-emptyinfo"]')
        return dict(empty=True if r else False)
