from django.db import models
from django.conf import settings
from marktplace.models import Offer

# Create your models here.
class Review(models.Model):
    product = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="review_user")
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
