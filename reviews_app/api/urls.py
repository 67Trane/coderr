from django.urls import path
from .views import ReviewView, ReviewDetailView

"""
URL patterns for the reviews_app API.

Defines REST endpoints under the '/api/' prefix for managing customer reviews of business users.

Endpoints:
    GET, POST   /api/reviews/         -> ReviewView: List all reviews or submit a new review (customers only).
    GET, PUT, PATCH, DELETE /api/reviews/<pk>/ -> ReviewDetailView: Retrieve, update, or delete a specific review (only by the original reviewer).

Naming conventions:
    'reviews'         - Collection endpoint for reviews.
    'reviews-detail'  - Detail endpoint for individual review operations (same name used for both paths for simplicity).

Permissions:
    - ReviewView: IsAuthenticated and IsCustomerOrReadOnly (authenticated customers may post reviews).
    - ReviewDetailView: IsAuthenticated and IsReviewer (only the assigned reviewer may modify or delete).
"""
urlpatterns = [
    # List existing reviews or create a new review
    path("reviews/", ReviewView.as_view(), name="reviews"),
    # Retrieve, update, or delete a specific review by ID
    path("reviews/<int:pk>/", ReviewDetailView.as_view(), name="reviews-detail"),
]
