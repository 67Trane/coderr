from django.db import models
from django.conf import settings

OFFER_TYPES = (
    ("basic", "Basic"),
    ("standard", "Standard"),
    ("premium", "Premium"),
)


class Offer(models.Model):
    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="offer_as_business",
        limit_choices_to={"type": "business"},
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="offer_images/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_details = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)


class OfferDetail(models.Model):
    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name="details")
    title = models.CharField(max_length=255, null=True, blank=True)
    revisions = models.PositiveIntegerField(default=0)
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list, blank=True)
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPES)
    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="business_user",
        limit_choices_to={"type": "business"},
    )
