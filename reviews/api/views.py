from rest_framework import generics
from .serializers import ReviewSerializer
from reviews.models import Review
from rest_framework.permissions import IsAuthenticatedOrReadOnly    

class ReviewView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
