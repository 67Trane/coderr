from rest_framework import generics, permissions
from .serializers import ReviewSerializer
from reviews_app.models import Review
from core.permissions import IsCustomerOrReadOnly, IsReviewer

"""
API views for the reviews_app, managing listing, creation, retrieval, updating, and deletion of Review instances.

Views:
    ReviewView: List all reviews or create a new review by a customer.
    ReviewDetailView: Retrieve, update, or delete a specific review by its ID.
"""


class ReviewView(generics.ListCreateAPIView):
    """
    GET: List all reviews across business users.
    POST: Create a new review by the authenticated customer.

    Permissions:
        - IsAuthenticated: Only logged-in users can list and create.
        - Write operations (POST) allowed for customers via IsCustomerOrReadOnly.

    Serializer:
        ReviewSerializer for input validation and output representation.

    Behavior:
        perform_create: Automatically assign the request.user as 'reviewer'.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomerOrReadOnly]

    def perform_create(self, serializer):
        """
        Save the new Review with the request.user set as the reviewer.

        Args:
            serializer: ReviewSerializer instance with validated data.
        """
        reviewer = self.request.user
        serializer.save(reviewer=reviewer)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a single Review by its ID with full details.
    PUT/PATCH: Update the review, only allowed for the assigned reviewer via IsReviewer.
    DELETE: Delete the review, only allowed for the assigned reviewer via IsReviewer.

    Permissions:
        - IsAuthenticated: Must be logged in.
        - IsReviewer: Reviewer must match request.user for non-safe methods.

    Serializer:
        ReviewSerializer for full Review data representation.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsReviewer]
