from rest_framework import serializers
from profile_app.models import Profile

"""
Serializers for the profile_app, managing representation and updates of user profiles.

This module defines:
    ProfileSerializer: Serializes Profile data combined with related User fields.
"""


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model, including nested User information.

    Provides read and write access to profile-specific fields and controlled updates for user fields.

    Fields:
        user (int): Read-only ID of the related User.
        username (str): Read-only username of the related User.
        email (str): User's email address (writable).
        type (str): Read-only user type ('business' or 'customer').
        first_name (str): User's first name (optional, writable).
        last_name (str): User's last name (optional, writable).
        created_at (datetime): Read-only timestamp of User.date_joined.
        file (ImageField): Profile image (optional).
        location (str): Profile location (optional).
        tel (str): Profile telephone number (optional).
        description (str): Profile description (optional).
        working_hours (str): Profile working hours (optional).
    """

    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email")
    type = serializers.CharField(source="user.type", read_only=True)
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)
    created_at = serializers.DateTimeField(source="user.date_joined", read_only=True)

    file = serializers.ImageField(required=False, allow_null=True)
    location = serializers.CharField(required=False, allow_null=True)
    tel = serializers.CharField(required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_null=True)
    working_hours = serializers.CharField(required=False)

    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at",
        ]

    def update(self, instance, validated_data):
        """
        Update Profile and nested User fields based on validated data.

        - User fields (first_name, last_name, email) are updated if present.
        - Profile-specific fields (file, location, tel, description, working_hours) are updated accordingly.

        Args:
            instance (Profile): The Profile instance to update.
            validated_data (dict): Validated data, may include nested 'user' dict.

        Returns:
            Profile: The updated profile instance.
        """
        user_data = validated_data.pop("user", {})

        if user_data:
            user = instance.user

            # Update user attributes if provided
            first_name = user_data.get("first_name")
            last_name = user_data.get("last_name")
            email = user_data.get("email")

            if first_name is not None:
                user.first_name = first_name
            if last_name is not None:
                user.last_name = last_name
            if email is not None:
                user.email = email

            user.save()

        # Update profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
