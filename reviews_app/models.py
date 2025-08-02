from django.db import models
from django.conf import settings

"""
Data model for the reviews_app, representing customer reviews for business users.

Model:
    Review: Stores rating, reviewer, and description linked to business and customer users.
"""


class Review(models.Model):
    """
    Represents a customer's review of a business user.

    Attributes:
        business_user (ForeignKey): The business user being reviewed.
        rating (PositiveIntegerField): Numeric rating given by the reviewer.
        reviewer (ForeignKey): The customer user who wrote the review.
        description (TextField): Optional text description of the review.
        created_at (DateTimeField): Timestamp when the review was created.
        updated_at (DateTimeField): Timestamp when the review was last updated.
    """

    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="review_user",
        limit_choices_to={"type": "business"},
        help_text="Business user who is being reviewed",
    )
    rating = models.PositiveIntegerField(
        help_text="Rating given by the customer (e.g., 1-5)",
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="reviewer_user",
        limit_choices_to={"type": "customer"},
        help_text="Customer user who wrote this review",
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Optional textual description of the review",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when this review was created",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when this review was last updated",
    )

    def __str__(self):
        """
        String representation of the Review.

        Returns:
            str: 'Review {id} by {reviewer.username} for {business_user.username}'.
        """
        reviewer_name = self.reviewer.username if self.reviewer else "Unknown"
        business_name = self.business_user.username if self.business_user else "Unknown"
        return f"Review {self.id} by {reviewer_name} for {business_name}"
