from django.db import models
from django.conf import settings


class Profile(models.Model):
    TYPES = (
        ("business", "Business"),
        ("customer", "Customer")
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    type = models.CharField(max_length=20, choices=TYPES, default="customer")