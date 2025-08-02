from django.urls import path
from .views import OrderListView, OrderDetailView, OrderCountView, OrderCompletedView

"""
URL patterns for the orders_app API.

Defines endpoints under the '/api/' prefix for managing orders and retrieving order statistics.

Endpoints:
    GET, POST   /api/orders/                       -> OrderListView: List user-specific orders or create a new order (customers only).
    GET, PUT, PATCH, DELETE /api/orders/<pk>/      -> OrderDetailView: Retrieve, update, or delete a specific order.
    GET          /api/order-count/<pk>/           -> OrderCountView: Get count of in-progress orders for a business user.
    GET          /api/completed-order-count/<pk>/ -> OrderCompletedView: Get count of completed orders for a business user.

Naming conventions:
    'orders'                  - Collection endpoint for orders.
    'order-detail'            - Detail endpoint for individual orders.
    'order-count'             - Endpoint for in-progress order count.
    'completed-order-count'   - Endpoint for completed order count.
"""
urlpatterns = [
    # List all orders for the user and create a new order
    path("orders/", OrderListView.as_view(), name="orders"),
    # Retrieve, update, or delete a specific order by ID
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    # Get count of 'in_progress' orders for a business user
    path("order-count/<int:pk>/", OrderCountView.as_view(), name="order-count"),
    # Get count of 'completed' orders for a business user
    path(
        "completed-order-count/<int:pk>/",
        OrderCompletedView.as_view(),
        name="completed-order-count",
    ),
]
