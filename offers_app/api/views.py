from rest_framework import generics
from django.db.models import Q
from offers_app.models import *
from .serializers import *
from rest_framework import permissions
from .pagination import StandardResultsSetPagination
from core.permissions import (
    IsBusinessOrReadOnly,
    IsOfferOwner,
)
from django.db.models import Min, Max
from rest_framework.exceptions import ParseError


class OffersListView(generics.ListCreateAPIView):
    queryset = Offer.objects.prefetch_related("details").all()
    serializer_class = OfferSerializer
    permission_classes = [IsBusinessOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(business_user=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        creator_id = params.get("creator_id")
        if creator_id:
            qs = qs.filter(business_user_id=creator_id)

        search = params.get("search")
        if search:
            qs = qs.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        ordering = params.get("ordering")
        if ordering:
            qs = qs.order_by(ordering)
        else:
            qs = qs.order_by("-created_at")

        qs = qs.annotate(
            min_price=Min("details__price"),
            min_delivery_time=Min("details__delivery_time_in_days")
        )

        delivery_max = params.get("max_delivery_time")
        if delivery_max:
            if not delivery_max.isdigit():
                raise ParseError("`max_delivery_time` must be an integer.")
            qs = qs.filter(min_delivery_time__lte=int(delivery_max))

        return qs


class SingleOfferView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated, IsOfferOwner]


class OfferDetailView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.AllowAny]


class OfferSingleDetailView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferSingleDetailSerializer
    permission_classes = [permissions.AllowAny]
