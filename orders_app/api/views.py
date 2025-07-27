from rest_framework import generics, status
from django.db.models import Q
from orders_app.models import *
from .serializers import *
from rest_framework import permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from reviews_app.models import Review
from profile_app.models import Profile
from core.permissions import (
    IsCustomerOrReadOnly,
    IsBusinessForUpdateOrAdminForDelete,
)
from authentication_app.models import User


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


class OrderCountView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(
        self,
        request,
        pk,
    ):
        get_object_or_404(User, pk=pk, type="business")
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
        get_object_or_404(User, pk=pk, type="business")
        current_user = Order.objects.filter(business_user=pk)
        count = current_user.filter(status="completed").count()
        data = {"completed_order_count": count}
        return Response(data, status=status.HTTP_200_OK)
