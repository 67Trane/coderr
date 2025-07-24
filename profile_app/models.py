from django.db import models
from django.utils import timezone
from core.settings import AUTH_USER_MODEL


class Profile(models.Model):
    user = models.OneToOneField(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile", default=1
    )
    file = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True, help_text="Profilbild."
    )
    location = models.CharField(
        max_length=255, blank=True, help_text="Adresse oder Standort"
    )
    tel = models.CharField(
        max_length=30, blank=True, help_text="Telefonnummer z.B. +49 123 4567 890"
    )
    description = models.TextField(blank=True, help_text="Beschreibung oder Bio")
    working_hours = models.CharField(help_text="Arbeitsstunden")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
