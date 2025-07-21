from rest_framework import viewsets
from profile_app.models import Profile
from authentication_app.models import User
from .serializers import (
    UserSerializer,
    RegistrationSerializer,
    ProfileSerializer,
    LoginSerializer,
)
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView
from django.contrib.auth import authenticate


class ProfileListView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if request.user.profile.id == int(kwargs["pk"]):
            return super().update(request, *args, **kwargs)

        return Response(
            {"detail": "Du darfst nur dein eigenes Profil bearbeiten."},
            status=status.HTTP_403_FORBIDDEN,
        )


class ProfileTypeListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile_type = self.kwargs.get("profile_type")
        return Profile.objects.filter(user__type=profile_type)




