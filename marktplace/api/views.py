from rest_framework import generics, status
from django.db.models import Q
from marktplace.models import *
from .serializers import *
from rest_framework import permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .pagination import StandardResultsSetPagination
from reviews.models import Review
from users.models import Profile


class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]

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


class OrderDetailView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk)
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OffersListView(generics.ListCreateAPIView):
    queryset = Offer.objects.prefetch_related("details").all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.AllowAny]
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

        return qs


class SingleOfferView(generics.RetrieveAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.AllowAny]


class OfferDetailView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.AllowAny]


class OrderCountView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]

    def get(
        self,
        request,
        pk,
    ):
        count = Order.objects.filter(business_user=pk).count()
        data = {"order_count": count}

        return Response(data, status=status.HTTP_200_OK)


class OrderCompletedView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]

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
        avg = Review.objects.aggregate(average_rating=models.Avg("rating"))["average_rating"] or 0
        business_profile_count = Profile.objects.filter(user__type="business").count()
        offer_count = Offer.objects.count()
        
        
        data = {
            "review_count": review_count,
            "average_rating": avg,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count,
        }
        return Response(data, status=status.HTTP_200_OK)
