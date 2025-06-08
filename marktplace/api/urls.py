from django.urls import path
from .views import *


urlpatterns = [
    path("orders/", OrderListView.as_view(), name="orders"),
    path("offers/", OffersListView.as_view(), name="offers"),
    path("offers/<int:pk>/", SingleOfferView.as_view(), name= "offer-detail"),
    path("offerdetails/<int:pk>/", OfferDetailView.as_view(), name="offer-details"),
    path("offerdetails/", OfferDetailView.as_view(), name="offer-details")
]
