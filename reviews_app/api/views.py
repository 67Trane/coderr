from rest_framework import generics
from rest_framework.response import Response
from .serializers import ReviewSerializer
from reviews_app.models import Review
from rest_framework import permissions
from rest_framework import status
from orders_app.models import Offer
from core.permissions import IsCustomerOrReadOnly, IsReviewer


class ReviewView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomerOrReadOnly]

    def perform_create(self, serializer):
        reviewer = self.request.user
        serializer.save(reviewer=reviewer)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsReviewer]
