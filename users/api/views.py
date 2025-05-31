from rest_framework import viewsets
from users.models import User, Profile
from .serializers import UserSerializer, RegistrationSerializer, ProfileSerializer
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    # def post(self, request):
    #     serializer = RegistrationSerializer(data=request.data)

    #     if serializer.is_valid():
    #         saved_account = serializer.save()
    #         return Response(saved_account.data, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
