from rest_framework import generics, status, permissions
from django.db.models import Q
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from orders_app.models import Order
from .serializers import OrderSerializer
from core.permissions import IsCustomerOrReadOnly, IsBusinessForUpdateOrAdminForDelete
from authentication_app.models import User

"""
API views for the orders_app, handling listing, creation, retrieval, updates, deletion, and simple order statistics.

Views:
    OrderListView:
        - GET: List all orders related to the requesting user (as customer or business).
        - POST: Create a new order from an OfferDetail (customers only).
    OrderDetailView:
        - GET: Retrieve a single order by its ID.
        - PUT/PATCH: Update an existing order (business owner only).
        - DELETE: Delete an order (business owner or admin for delete operations).
    OrderCountView:
        - GET: Return count of in-progress orders for a given business user.
    OrderCompletedView:
        - GET: Return count of completed orders for a given business user.
"""


class OrderListView(generics.ListCreateAPIView):
    """
    GET: Return a list of Order instances related to the authenticated user.
        - Customers see their placed orders.
        - Business users see orders assigned to them.

    POST: Place a new order by providing an 'offer_detail_id'.
        - Requires authenticated customer (IsCustomerOrReadOnly).
        - Validates, creates the Order, and returns full representation.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomerOrReadOnly]

    def get_queryset(self):
        """
        Filter orders where the user is either the customer or business participant.

        Returns:
            QuerySet[Order]: Orders for the requesting user.
        """
        user = self.request.user
        return Order.objects.filter(Q(customer_user=user) | Q(business_user=user))

    def post(self, request, *args, **kwargs):
        """
        Create a new Order from validated input and return its serialized data.

        Steps:
            1. Validate input via OrderSerializer (context includes request).
            2. Save Order instance.
            3. Serialize and return the created Order with HTTP 201 status.
        """
        create_serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        create_serializer.is_valid(raise_exception=True)
        order = create_serializer.save()

        output_serializer = OrderSerializer(order)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve details of a specific Order by its primary key.
    PUT/PATCH: Update order fields (only allowed for the business user who owns the order).
    DELETE: Delete the order (business users for updates, admins may delete).

    Permissions:
        - IsBusinessForUpdateOrAdminForDelete: Enforces business update and staff delete rules.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsBusinessForUpdateOrAdminForDelete]

    def get(self, request, pk, *args, **kwargs):
        """
        Override GET to return serialized Order with HTTP 200.

        Raises:
            Http404: If no Order matches the provided pk.
        """
        order = get_object_or_404(Order, pk=pk)
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderCountView(generics.RetrieveAPIView):
    """
    GET: Retrieve the count of 'in_progress' orders for the specified business user.

    URL Param:
        pk (int): ID of the business user whose orders are counted.

    Returns:
        {'order_count': int} with HTTP 200.

    Permissions:
        - IsAuthenticated: User must be logged in.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        """
        Validate business user existence and count their in-progress orders.
        """
        get_object_or_404(User, pk=pk, type="business")
        count = Order.objects.filter(business_user=pk, status="in_progress").count()
        return Response({"order_count": count}, status=status.HTTP_200_OK)


class OrderCompletedView(generics.RetrieveAPIView):
    """
    GET: Retrieve the count of 'completed' orders for the specified business user.

    URL Param:
        pk (int): ID of the business user whose completed orders are counted.

    Returns:
        {'completed_order_count': int} with HTTP 200.

    Permissions:
        - IsAuthenticated: User must be logged in.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        """
        Validate business user existence and count their completed orders.
        """
        get_object_or_404(User, pk=pk, type="business")
        count = Order.objects.filter(business_user=pk, status="completed").count()
        return Response({"completed_order_count": count}, status=status.HTTP_200_OK)
