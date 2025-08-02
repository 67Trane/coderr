from .serializers import UserSerializer, LoginSerializer, RegistrationSerializer
from profile_app.models import Profile
from rest_framework import permissions, generics, status
from authentication_app.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate

"""
API views for user management, including registration, login, and profile access.

This module provides:
- UserView: List and create Users.
- UserDetailView: Retrieve details of the currently authenticated user.
- LoginView: Authenticate users and return a token.
- RegistrationView: Register new users and create associated Profiles.
"""


class UserView(generics.ListCreateAPIView):
    """
    GET: List all users.
    POST: Create a new user.

    Permissions:
        AllowAny: Publicly accessible.

    Serializer:
        UserSerializer for both listing and creation.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserDetailView(generics.RetrieveAPIView):
    """
    GET: Retrieve the currently authenticated user's details.

    Permissions:
        AllowAny: Publicly accessible, but returns only the requesting user.

    Serializer:
        UserSerializer for user representation.
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        """
        Override to return the request's user instance.

        Returns:
            User: The currently authenticated user.
        """
        return self.request.user


class LoginView(APIView):
    """
    POST: Authenticate a user and return an auth token and basic user info.

    Permissions:
        AllowAny: Publicly accessible.

    Request Body:
        username (str): User's username.
        password (str): User's password.

    Responses:
        200 OK: { token, user_id, username, email }
        400 Bad Request: Validation errors.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Validate credentials and authenticate the user.

        Args:
            request: HTTP request containing 'username' and 'password'.

        Returns:
            Response: JSON with auth token and user data, or errors.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            user = authenticate(
                username=username, password=request.data.get("password")
            )
            token = serializer.validated_data["token"]
            return Response(
                {
                    "token": token,
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationView(generics.CreateAPIView):
    """
    POST: Register a new user and create an associated profile.

    Permissions:
        AllowAny: Publicly accessible.

    Request Body:
        username (str), email (str), type (str), password (str).

    Responses:
        201 Created: Serialized user data with token.
        400 Bad Request: Validation errors.
    """

    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Validate registration data, save new User, and create a Profile.

        Args:
            request: HTTP request with registration fields.

        Returns:
            Response: Serialized user data or errors.
        """
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            new_user = serializer.save()
            # Automatically create a Profile for the new user
            Profile.objects.create(user=new_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
