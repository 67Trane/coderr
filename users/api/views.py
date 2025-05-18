from rest_framework import viewsets
from users.models import BusinessProfile
from .serializers import BusinessSerializer



class BusinessProfileView(viewsets.ModelViewSet):
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessSerializer