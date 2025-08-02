from django.urls import path
from .views import (
    OffersListView,
    SingleOfferView,
    OfferDetailView,
    OfferSingleDetailView,
)

"""
URL patterns for the offers_app API.

Defines endpoints under the '/api/' prefix for managing service offers and their details.

Endpoints:
    GET, POST /api/offers/                 -> OffersListView: List existing offers or create a new one (business users).
    GET, PUT, PATCH, DELETE /api/offers/<pk>/ -> SingleOfferView: Retrieve, update, or delete a specific offer.
    GET /api/offerdetails/                 -> OfferDetailView: Retrieve minimal representations of offer detail entries.
    GET /api/offerdetails/<pk>/            -> OfferSingleDetailView: Retrieve full detail for a specific OfferDetail.

Naming conventions:
    'offers'              - Base endpoint for offer collection.
    'offer-detail'        - Detail endpoint for individual offers.
    'offerdetails'        - Base endpoint for offer details list.
    'offerdetails-details'- Detail endpoint for individual offer details.
"""
urlpatterns = [
    # List and create offers
    path("offers/", OffersListView.as_view(), name="offers"),
    # Retrieve, update, or delete a specific offer by ID
    path("offers/<int:pk>/", SingleOfferView.as_view(), name="offer-detail"),
    # List minimal offer detail representations
    path("offerdetails/", OfferDetailView.as_view(), name="offerdetails"),
    # Retrieve full details for a specific offer detail by ID
    path(
        "offerdetails/<int:pk>/",
        OfferSingleDetailView.as_view(),
        name="offerdetails-details",
    ),
]
