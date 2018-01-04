from django.db import models

# Create your models here.

class Offer(models.Model):
    offer_id = models.CharField(max_length=32, db_index=True, unique=True)
    offer_name = models.CharField(max_length=255)
    offer_url = models.CharField(max_length=4000)
    offer_price = models.IntegerField()

    car_brand = models.CharField(max_length=255)
    car_model = models.CharField(max_length=255)
    
    dealer_phone = models.CharField(max_length=32)
    dealer_name = models.CharField(max_length=255)

    import_date = models.DateTimeField()
    sell_date = models.DateTimeField(null=True)
    sold = models.BooleanField(default=False)
