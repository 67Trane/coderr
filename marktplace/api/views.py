from rest_framework import generics, status
from django.db.models import Q
from marktplace.models import *
from .serializers import *
from rest_framework import permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .pagination import StandardResultsSetPagination


class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        offer_detail_id = request.data.get("offer_detail_id")
        if offer_detail_id is None:
            return Response({"detail": "offer_detail_id fehlt."}, status=status.HTTP_400_BAD_REQUEST)

        offer_detail = get_object_or_404(Offer, pk=offer_detail_id)
        user = request.user
        if not hasattr(user, "type") or user.type != "customer":
            return Response({"detail": "Nur Customer dürfen bestellen"}, status=status.HTTP_403_FORBIDDEN)

        new_order = Order.objects.create(
            customer_user=user,
            business_user=offer_detail.business_user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
        )

        serializer = self.get_serializer(new_order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OffersListView(generics.ListCreateAPIView):
    queryset = Offer.objects.prefetch_related('details').all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(business_user=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        creator_id = params.get('creator_id')
        if creator_id:
            qs = qs.filter(business_user_id=creator_id)

        search = params.get('search')
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        ordering = params.get('ordering')
        if ordering:
            qs = qs.order_by(ordering)
        else:
            qs = qs.order_by('-created_at')

        return qs


class SingleOfferView(generics.RetrieveAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.AllowAny]


class OfferDetailView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.AllowAny]
    
    


