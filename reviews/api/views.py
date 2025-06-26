from rest_framework import generics
from rest_framework.response import Response
from .serializers import ReviewSerializer
from reviews.models import Review
from rest_framework import permissions
from rest_framework import status
from marktplace.models import Offer
from freelancer.permissions import IsCustomerOrReadOnly, IsReviewer


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
