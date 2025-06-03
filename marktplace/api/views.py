from rest_framework import generics, status
from marktplace.models import *
from .serializers import *
from rest_framework import permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


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
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.AllowAny]
