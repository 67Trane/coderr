from django.urls import path
from .views import *


urlpatterns = [
    
    path("orders/", OrderListView.as_view(), name="orders"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("offers/", OffersListView.as_view(), name="offers"),
    path("offers/<int:pk>/", SingleOfferView.as_view(), name="offer-detail"),
    path(
        "offerdetails/<int:pk>/", OfferDetailView.as_view(), name="offerdetails-details"
    ),
    path("offerdetails/", OfferDetailView.as_view(), name="offerdetails-details"),
    path("order-count/<int:pk>/", OrderCountView.as_view(), name="order-count"),
    path(
        "completed-order-count/<int:pk>/",
        OrderCompletedView.as_view(),
        name="completed-order-count",
    ),
    
    path("base-info/", BaseInfos.as_view(), name="base-infos"),
]
