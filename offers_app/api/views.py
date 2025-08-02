from rest_framework import generics, permissions
from django.db.models import Q, Min
from rest_framework.exceptions import ParseError, PermissionDenied
from django.shortcuts import get_object_or_404

from offers_app.models import Offer, OfferDetail
from .serializers import (
    OfferSerializer,
    OfferDetailSerializer,
    OfferSingleDetailSerializer,
)
from .pagination import StandardResultsSetPagination
from core.permissions import IsBusinessOrReadOnly, IsOfferOwner

"""
API views for offers_app: listing, creating, retrieving, updating, and deleting offers and offer details.

Classes:
    OffersListView:
        - GET: List offers with filtering (creator_id, search), ordering, pagination, and annotated fields (min_price, min_delivery_time).
        - POST: Create an offer by authenticated business users.

    SingleOfferView:
        - GET: Retrieve a single offer with annotated fields.
        - PUT/PATCH: Update an offer (only by authenticated owner via IsOfferOwner).
        - DELETE: Delete an offer (only by business users; enforced in destroy).

    OfferDetailView:
        - GET: Retrieve minimal hyperlinked representation of an OfferDetail.

    OfferSingleDetailView:
        - GET: Retrieve full detail fields for an OfferDetail.
"""


class OffersListView(generics.ListCreateAPIView):
    """
    GET: Paginated list of offers with optional filters and ordering.
    POST: Create a new offer linked to the requesting business user.

    Permissions:
        - SAFE_METHODS: Public read access.
        - POST: Authenticated business users only (IsBusinessOrReadOnly).

    Query Params:
        creator_id (int): Filter by business_user id.
        search (str): Case-insensitive search on title and description.
        ordering (str): Ordering field (e.g., '-created_at'). Defaults to '-created_at'.
        max_delivery_time (int): Filter offers with annotated min_delivery_time <= value.
        min_price (int): Filter offers with annotated min_price >= value.

    Annotations:
        min_price: Minimum price among related OfferDetail items.
        min_delivery_time: Minimum delivery_time_in_days among related OfferDetail items.

    Pagination:
        StandardResultsSetPagination (default page_size=2).
    """

    queryset = Offer.objects.prefetch_related("details").all()
    serializer_class = OfferSerializer
    permission_classes = [IsBusinessOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        """
        Assign the requesting user as the business_user when creating an offer.

        Args:
            serializer: OfferSerializer instance containing validated data.
        """
        serializer.save(business_user=self.request.user)

    def get_queryset(self):
        """
        Apply filters, search, ordering, and annotations to the base queryset.

        Returns:
            QuerySet[Offer]: Annotated and filtered offers.
        """
        qs = super().get_queryset()
        params = self.request.query_params

        creator_id = params.get("creator_id")
        if creator_id:
            qs = qs.filter(business_user_id=creator_id)

        search = params.get("search")
        if search:
            qs = qs.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        ordering = params.get("ordering")
        if ordering:
            qs = qs.order_by(ordering)
        else:
            qs = qs.order_by("-created_at")

        # Annotate aggregated fields
        qs = qs.annotate(
            min_price=Min("details__price"),
            min_delivery_time=Min("details__delivery_time_in_days"),
        )

        delivery_max = params.get("max_delivery_time")
        if delivery_max:
            if not delivery_max.isdigit():
                raise ParseError("`max_delivery_time` must be an integer.")
            qs = qs.filter(min_delivery_time__lte=int(delivery_max))

        min_price = params.get("min_price")
        if min_price:
            if not min_price.isdigit():
                raise ParseError("`min_price` must be an integer.")
            qs = qs.filter(min_price__gte=int(min_price))

        return qs


class SingleOfferView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve details of a single offer with nested details and annotated metrics.
    PUT/PATCH: Update the offer (owned by the business user).
    DELETE: Delete the offer (business users only; enforced via PermissionDenied override).

    Permissions:
        - SAFE_METHODS: Authenticated users.
        - UPDATE/DELETE: Owner or staff (IsOfferOwner for object-level checks, additional destroy logic).

    Queryset:
        Annotated with min_price and min_delivery_time.
    """

    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated | IsOfferOwner]

    def get_queryset(self):
        """
        Provide annotated queryset for retrieving an offer.

        Returns:
            QuerySet[Offer]: Offers annotated with aggregate metrics.
        """
        return Offer.objects.annotate(
            min_price=Min("details__price"),
            min_delivery_time=Min("details__delivery_time_in_days"),
        )

    def destroy(self, request, *args, **kwargs):
        """
        Enforce that only users with type 'business' may delete offers.

        Raises:
            PermissionDenied: If user is not a 'business' type.
        """
        if getattr(request.user, "type", None) != "business":
            raise PermissionDenied("You do not have permission to delete offers.")
        return super().destroy(request, *args, **kwargs)


class OfferDetailView(generics.RetrieveAPIView):
    """
    GET: Retrieve a minimal hyperlinked representation of a specific OfferDetail.

    Permissions:
        - IsAuthenticated: Require login.

    Serializer:
        OfferDetailSerializer: Provides 'id' and 'url' fields.
    """

    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class OfferSingleDetailView(generics.RetrieveAPIView):
    """
    GET: Retrieve full details of a specific OfferDetail instance.

    Permissions:
        - IsAuthenticated: Require login.

    Serializer:
        OfferSingleDetailSerializer: Exposes all detail fields.
    """

    queryset = OfferDetail.objects.all()
    serializer_class = OfferSingleDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
