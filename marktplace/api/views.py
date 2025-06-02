from rest_framework import generics
from marktplace.models import Order
from .serializers import OrderSerializer
from rest_framework import permissions


class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]