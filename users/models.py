from django.db import models


class BusinessProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    orders = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    reviews = models.CharField(max_length=200)


class CustomerProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    orders = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    reviews = models.CharField(max_length=200)
