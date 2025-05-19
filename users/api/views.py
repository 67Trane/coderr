from rest_framework import viewsets
from users.models import BusinessProfile
from .serializers import BusinessSerializer
from rest_framework import generics



class BusinessProfileView(generics.ListCreateAPIView):
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessSerializer
    