from django.urls import path
from .views import *


urlpatterns = [
    path("reviews/", ReviewView.as_view(), name="reviews"),
    path("reviews/<int:pk>/", ReviewDetailView.as_view(), name="reviews"),
]
