from django.shortcuts import render
from django.views import generic
from django.db.models import Avg, Sum, Min, Max

from .models import Offer

# Create your views here.

def index(request):
    return render(request, 'index.html')


class OffersList(generic.ListView):
    template_name = 'offers.html'
    context_object_name = 'offers'

    def get_queryset(self):
        return Offer.objects.all()


class ModelsList(generic.ListView):
    template_name = 'models.html'
    context_object_name = 'models'

    def get_queryset(self):
        return Offer.objects.values('car_model').annotate(
            Sum('offer_price'), Avg('offer_price'), Min('offer_price'), Max('offer_price'))
