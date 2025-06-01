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
    

class GuestCustomer(models.Model):
    username = models.CharField(max_length=200, default="andrey")
    password = models.CharField(max_length=200, default="asdasd")
    
class GuestBusiness(models.Model):
    username = models.CharField(max_length=200, default="kevin")
    password = models.CharField(max_length=200, default="asdasd24")