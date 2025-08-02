from django.db import models
from django.conf import settings
from offers_app.models import OfferDetail

"""
Data models for the orders_app, defining order tracking and lifecycle for OfferDetail purchases.

Models:
    Order: Represents a purchase request by a customer for a specific OfferDetail, linking customer and business users, pricing, timing, and status.

Constants:
    STATUS_TYPES: Allowed order statuses ('in_progress', 'completed', 'cancelled').
"""


STATUS_TYPES = (
    ("in_progress", "In Progress"),
    ("completed", "Completed"),
    ("cancelled", "Cancelled"),
)


class Order(models.Model):
    """
    Represents an order placed by a customer for a specific OfferDetail from a business.

    Attributes:
        customer_user (ForeignKey): Link to the User (type='customer') who placed this order.
        business_user (ForeignKey): Link to the User (type='business') fulfilling this order.
        title (CharField): Title copied from the related OfferDetail.
        revisions (PositiveIntegerField): Number of allowed revisions from the OfferDetail.
        delivery_time_in_days (IntegerField): Expected delivery time copied from the OfferDetail.
        price (DecimalField): Price copied from the OfferDetail.
        features (JSONField): List of features description from the OfferDetail.
        offer_type (CharField): Type of the offer tier from the OfferDetail.
        created_at (DateTimeField): Timestamp when the order was created.
        updated_at (DateTimeField): Timestamp when the order was last updated.
        status (CharField): Current status of the order, one of STATUS_TYPES.
        offer_detail (ForeignKey): Reference to the OfferDetail instance this order is based on.
    """

    customer_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders_as_customer",
        limit_choices_to={"type": "customer"},
        blank=True,
        null=True,
        help_text="Customer who placed this order",
    )
    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders_as_business",
        limit_choices_to={"type": "business"},
        blank=True,
        null=True,
        help_text="Business user responsible for fulfilling this order",
    )
    title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Title inherited from the ordered OfferDetail",
    )
    revisions = models.PositiveIntegerField(
        default=0,
        help_text="Number of revision rounds allowed (from OfferDetail)",
    )
    delivery_time_in_days = models.IntegerField(
        null=True,
        blank=True,
        help_text="Expected delivery time in days (from OfferDetail)",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Price for the order (from OfferDetail)",
    )
    features = models.JSONField(
        default=list,
        blank=True,
        help_text="JSON list of feature descriptions (from OfferDetail)",
    )
    offer_type = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        help_text="Tier type of the order (from OfferDetail)",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
        help_text="Timestamp when this order was created",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when this order was last updated",
    )
    status = models.CharField(
        max_length=100,
        choices=STATUS_TYPES,
        default="in_progress",
        help_text="Current status of the order",
    )
    offer_detail = models.ForeignKey(
        OfferDetail,
        on_delete=models.CASCADE,
        related_name="order_details",
        null=True,
        blank=True,
        help_text="Reference to the specific OfferDetail this order is based on",
    )
