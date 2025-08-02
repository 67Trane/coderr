from django.db import models
from django.contrib.auth.models import AbstractUser

"""
Custom User model extending Django's AbstractUser.

Defines a 'type' field to distinguish between business and customer users.

Fields:
    username, password, email, etc. (inherited from AbstractUser)
    type (str): Role of the user, either 'business' or 'customer'.
"""


class User(AbstractUser):
    """
    Custom user model with additional 'type' field.

    Attributes:
        TYPES (tuple): Available user roles as (value, display_name).
        type (CharField): Role of the user, defaults to 'customer'.
    """

    TYPES = (
        ("business", "Business"),
        ("customer", "Customer"),
    )
    type = models.CharField(
        max_length=20,
        choices=TYPES,
        default="customer",
        help_text="Specifies the role of the user, either 'business' or 'customer'.",
    )
