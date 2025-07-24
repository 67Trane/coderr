from django.db import models
from django.conf import settings
from offers_app.models import OfferDetail

STATUS_TYPES = (
    ("in_progress", "In Progress"),
    ("completed", "Completed"),
    ("cancelled", "Cancelled"),
)


class Order(models.Model):
    customer_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders_as_customer",
        limit_choices_to={"type": "customer"},
        blank=True,
        null=True,
    )
    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders_as_business",
        limit_choices_to={"type": "business"},
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    revisions = models.PositiveIntegerField(default=0)
    delivery_time_in_days = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    features = models.JSONField(default=list, blank=True)
    offer_type = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=100, choices=STATUS_TYPES, default="in_progress"
    )
    offer_detail = models.ForeignKey(
        OfferDetail,
        on_delete=models.CASCADE,
        related_name="offer_details",
        null=True,
        blank=True,
    )
