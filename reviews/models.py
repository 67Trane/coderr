from django.db import models
from django.conf import settings
from marktplace.models import Offer

# Create your models here.
class Review(models.Model):
    product = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="offer")
    business_user = models.ForeignKey(settings.AUTH_USER_MODEL,blank=True, null=True, on_delete=models.CASCADE, related_name="review_user", limit_choices_to={'type': 'business'})
    rating = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
