from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    TYPES = (("business", "Business"), ("customer", "Customer"))
    type = models.CharField(max_length=20, choices=TYPES, default="customer")


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", default=1
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


class GuestCustomer(models.Model):
    username = models.CharField(max_length=200, default="andrey")
    password = models.CharField(max_length=200, default="asdasd")


class GuestBusiness(models.Model):
    username = models.CharField(max_length=200, default="kevin")
    password = models.CharField(max_length=200, default="asdasd24")
