from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    TYPES = (
        ("business", "Business"),
        ("customer", "Customer")
    )
    type = models.CharField(max_length=20, choices=TYPES, default="customer")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", default=1)
    
