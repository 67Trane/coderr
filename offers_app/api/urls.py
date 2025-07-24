from django.urls import path
from .views import *


urlpatterns = [
    path("offers/", OffersListView.as_view(), name="offers"),
    path("offers/<int:pk>/", SingleOfferView.as_view(), name="offer-detail"),
    path(
        "offerdetails/<int:pk>/",
        OfferSingleDetailView.as_view(),
        name="offerdetails-details",
    ),
    path("offerdetails/", OfferDetailView.as_view(), name="offerdetails-details"),
]
