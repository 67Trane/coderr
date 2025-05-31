from django.db import models
from django.contrib.auth.models import AbstractUser
TYPES = (
        ("business", "Business"),
        ("customer", "Customer")
    )

class User(AbstractUser):
    type = models.CharField(max_length=20, choices=TYPES, default="customer")

class Profile(models.Model):
    username=models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    type = models.CharField(max_length=20 , choices=TYPES, default="customer")