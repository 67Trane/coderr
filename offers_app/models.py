from django.db import models
from django.conf import settings

"""
Data models for the offers_app, defining offers and their detailed variants.

Models:
    Offer: Represents a listing created by a business user with a title, description, image, and timestamps.
    OfferDetail: Represents a specific package or tier of an Offer, including pricing, delivery time, and features.

Constants:
    OFFER_TYPES: Available tiers for an OfferDetail ('basic', 'standard', 'premium').
"""


OFFER_TYPES = (
    ("basic", "Basic"),
    ("standard", "Standard"),
    ("premium", "Premium"),
)


class Offer(models.Model):
    """
    Core model for offers made by business users.

    Attributes:
        business_user (ForeignKey): Link to the User (type='business') who created the offer.
        title (CharField): Optional title of the offer.
        image (ImageField): Optional image uploaded for the offer.
        description (TextField): Optional detailed description.
        created_at (DateTimeField): Timestamp when the offer was created.
        updated_at (DateTimeField): Timestamp when the offer was last modified.
        user_details (ForeignKey): Legacy or auxiliary link to a User; typically unused if using business_user.
    """

    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="offer_as_business",
        limit_choices_to={"type": "business"},
        help_text="The business user who owns this offer",
    )
    title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Optional title of the offer",
    )
    image = models.ImageField(
        upload_to="offer_images/",
        null=True,
        blank=True,
        help_text="Optional image for the offer, stored under 'offer_images/'",
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Optional detailed description of the offer",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
        help_text="Timestamp when the offer was first created",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the offer was last updated",
    )
    user_details = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="Auxiliary link to a User; not used for business ownership",
    )


class OfferDetail(models.Model):
    """
    Represents a tiered package or detail option for a parent Offer.

    Attributes:
        offer (ForeignKey): Parent Offer this detail belongs to.
        title (CharField): Optional title for this detail package.
        revisions (PositiveIntegerField): Number of allowed revisions included.
        delivery_time_in_days (IntegerField): Expected delivery time in days.
        price (DecimalField): Cost of this detail package.
        features (JSONField): List of feature descriptions for this package.
        offer_type (CharField): Tier type, one of 'basic', 'standard', or 'premium'.
        business_user (ForeignKey): Business user owning this particular detail.
    """

    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="details",
        help_text="Parent offer for this detail package",
    )
    title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Optional title for this detail",
    )
    revisions = models.PositiveIntegerField(
        default=0,
        help_text="Number of revision rounds allowed",
    )
    delivery_time_in_days = models.IntegerField(
        null=True,
        help_text="Expected delivery time in days",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price for this detail package",
    )
    features = models.JSONField(
        default=list,
        blank=True,
        help_text="JSON list of feature descriptions for this package",
    )
    offer_type = models.CharField(
        max_length=10,
        choices=OFFER_TYPES,
        help_text="Tier of the detail (basic, standard, premium)",
    )
    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="business_user",
        limit_choices_to={"type": "business"},
        help_text="Business user associated with this detail",
    )
