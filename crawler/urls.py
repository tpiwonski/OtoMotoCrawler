from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('offers/', views.OffersList.as_view(), name='offers'),
    path('models/', views.ModelsList.as_view(), name='models')
]
