from django.urls import path
from .views import *


urlpatterns = [
    path("orders/", OrderListView.as_view(), name="orders"),
    path("offers/", OffersListView.as_view(), name="offers"),
    path("offers/<int:pk>/", OfferDetailView.as_view(), name= "offer-detail")
]
