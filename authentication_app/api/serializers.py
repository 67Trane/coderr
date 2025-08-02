from authentication_app.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

"""
Serializers for user registration, authentication, and representation in the authentication_app.

This module defines:
- UserSerializer: Exposes all fields of the User model.
- RegistrationSerializer: Handles new user sign-up with password hashing and token generation.
- LoginSerializer: Validates credentials and returns an auth token.
"""


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model including all fields for full representation.

    Fields:
        All fields defined on the User model.
    """

    class Meta:
        model = User
        fields = "__all__"


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for handling user registration.

    - Accepts username, email, type, and password.
    - Returns user_id and authentication token upon successful creation.
    """

    password = serializers.CharField(write_only=True)
    user_id = serializers.IntegerField(source="id", read_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "type", "user_id", "password", "token"]

    def create(self, validated_data):
        """
        Create a new User instance, set and hash the password, and generate a Token.

        Args:
            validated_data (dict): Validated serializer data including 'username', 'email', 'type', and 'password'.

        Returns:
            User: The created user instance with attached 'token' attribute.
        """
        pwd = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(pwd)
        user.save()

        token, _ = Token.objects.get_or_create(user=user)
        user.token = token.key
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login, validates credentials, and returns token.

    - write_only fields: 'username' and 'password'.
    - read_only field: 'token'.
    """

    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        """
        Authenticate user with provided credentials and return auth token.

        Args:
            data (dict): Contains 'username' and 'password'.

        Raises:
            serializers.ValidationError: If credentials are invalid or account is inactive.

        Returns:
            dict: Original data augmented with 'token'.
        """
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("Benutzerkonto ist deaktiviert.")
                token_obj, _ = Token.objects.get_or_create(user=user)
                data["token"] = token_obj.key
                return data
            else:
                raise serializers.ValidationError(
                    "Ungültiger Benutzername oder Passwort"
                )
        else:
            raise serializers.ValidationError(
                "Beide Felder (username, password) sind erforderlich."
            )
