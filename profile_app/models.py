from django.db import models
from django.utils import timezone
from core.settings import AUTH_USER_MODEL

"""
Data model for the profile_app, representing user profile information linked to the custom User model.

Model:
    Profile: Stores profile picture, contact details, description, and working hours for each User.
"""


class Profile(models.Model):
    """
    Extends user data with profile-specific attributes.

    Attributes:
        user (OneToOneField): Link to the authenticated User (One-to-One relationship).
        file (ImageField): Optional profile picture uploaded to 'profile_pictures/'.
        location (CharField): Optional address or location description.
        tel (CharField): Optional phone number (e.g., '+49 123 4567 890').
        description (TextField): Optional bio or description text.
        working_hours (CharField): Required working hours schedule description.
        created_at (DateTimeField): Timestamp when the profile was created.
        updated_at (DateTimeField): Timestamp when the profile was last updated.
    """

    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        default=1,
        help_text="One-to-one link to the User account",
    )
    file = models.ImageField(
        upload_to="profile_pictures/",
        null=True,
        blank=True,
        help_text="Optional profile image stored under 'profile_pictures/'",
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional address or location description",
    )
    tel = models.CharField(
        max_length=30,
        blank=True,
        help_text="Optional telephone number, e.g., '+49 123 4567 890'",
    )
    description = models.TextField(
        blank=True,
        help_text="Optional profile description or biography",
    )
    working_hours = models.CharField(
        max_length=255,
        help_text="Working hours schedule description",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
        help_text="Timestamp when this profile was created",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when this profile was last updated",
    )

    def __str__(self):
        """
        String representation of the Profile.

        Returns:
            str: Username and ID of the associated user.
        """
        return f"Profile of {self.user.username} (ID: {self.user.id})"
