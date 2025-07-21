from rest_framework import generics, status
from django.db.models import Q
from orders_app.models import *
from .serializers import *
from rest_framework import permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .pagination import StandardResultsSetPagination
from reviews_app.models import Review
from profile_app.models import Profile
from core.permissions import (
    IsCustomerOrReadOnly,
    IsBusinessOrReadOnly,
    IsOfferOwner,
    IsBusinessForUpdateOrAdminForDelete,
)
from django.db.models import Min, Max
from rest_framework.exceptions import ParseError


class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(Q(customer_user=user) | (Q(business_user=user)))

    def post(self, request, *args, **kwargs):
        # Eingabe-Serializer validieren und Order erzeugen
        create_serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        create_serializer.is_valid(raise_exception=True)
        order = create_serializer.save()

        # Ausgabe-Serializer, um alle Felder zurückzugeben
        output_serializer = OrderSerializer(order)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsBusinessForUpdateOrAdminForDelete]

    def get(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk)
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


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

        qs = qs.annotate(min_price=Min("details__price"))
        qs = qs.annotate(min_delivery_time=Min(
            "details__delivery_time_in_days"))

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

    

class OrderCountView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(
        self,
        request,
        pk,
    ):
        count = Order.objects.filter(business_user=pk).count()
        data = {"order_count": count}

        return Response(data, status=status.HTTP_200_OK)


class OrderCompletedView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(
        self,
        request,
        pk,
    ):
        current_user = Order.objects.filter(business_user=pk)
        count = current_user.filter(status="completed").count()
        data = {"completed_order_count": count}

        return Response(data, status=status.HTTP_200_OK)


class BaseInfos(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        review_count = Review.objects.count()
        avg = (
            Review.objects.aggregate(average_rating=models.Avg("rating"))[
                "average_rating"
            ]
            or 0
        )
        business_profile_count = Profile.objects.filter(
            user__type="business").count()
        offer_count = Offer.objects.count()

        data = {
            "review_count": review_count,
            "average_rating": avg,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count,
        }
        return Response(data, status=status.HTTP_200_OK)
