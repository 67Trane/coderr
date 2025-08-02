from rest_framework.permissions import BasePermission, SAFE_METHODS
from orders_app.models import Order
from rest_framework.exceptions import NotFound

"""
Custom permission classes for the Orders and Offers APIs.

This module defines several permission checks that enforce:
- Read-only access for all users on safe HTTP methods.
- Role-based access control for customers, reviewers, business users, and staff.
- Object-level permissions to ensure only the rightful owners or designated users may modify or delete resources.
"""


class IsCustomerOrReadOnly(BasePermission):
    """
    Allows full access to authenticated customers, and read-only access for everyone else.
    """

    def has_permission(self, request, view):
        """
        Permit safe (read-only) HTTP methods for any request.
        For write operations, ensure the user is authenticated and has the 'customer' type.

        Args:
            request: The HTTP request being processed.
            view: The view handling the request.

        Returns:
            bool: True if access should be granted, False otherwise.
        """
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.type == "customer"


class IsReviewer(BasePermission):
    """
    Allows reviewers to access and modify objects they are assigned to review.
    Read-only access is granted to any request.
    """

    def has_permission(self, request, view):
        """
        Permit safe (read-only) HTTP methods for any request.
        For write operations, ensure the user is authenticated (role-specific checks occur at object level).

        Args:
            request: The HTTP request being processed.
            view: The view handling the request.

        Returns:
            bool: True if access should be granted to proceed to object-level checks.
        """
        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Permit safe (read-only) HTTP methods for any request.
        For write operations, ensure the requesting user is the assigned reviewer of the object.

        Args:
            request: The HTTP request being processed.
            view: The view handling the request.
            obj: The object being accessed.

        Returns:
            bool: True if user is the reviewer of the object, False otherwise.
        """
        if request.method in SAFE_METHODS:
            return True

        return obj.reviewer == request.user


class IsBusinessOrReadOnly(BasePermission):
    """
    Allows full access to authenticated business users, and read-only access for everyone else.
    """

    def has_permission(self, request, view):
        """
        Permit safe (read-only) HTTP methods for any request.
        For write operations, ensure the user is authenticated and has the 'business' type.

        Args:
            request: The HTTP request being processed.
            view: The view handling the request.

        Returns:
            bool: True if access should be granted, False otherwise.
        """
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.type == "business"


class IsBusinessForUpdateOrAdminForDelete(BasePermission):
    """
    Grants update permissions to business users and delete permissions to staff users on Order instances.
    Read-only access is granted to any request.
    """

    def has_permission(self, request, view):
        """
        Permit safe (read-only) HTTP methods for any request.
        Verify that the Order exists for write operations, raising NotFound if missing.
        Allow PUT/PATCH only for authenticated business users.
        Allow DELETE only for authenticated staff users.

        Args:
            request: The HTTP request being processed.
            view: The view handling the request (contains URL kwargs).

        Raises:
            NotFound: If no Order with the given PK exists.

        Returns:
            bool: True if access should be granted, False otherwise.
        """
        if request.method in SAFE_METHODS:
            return True

        # Retrieve the primary key from URL kwargs (default 'pk')
        pk = view.kwargs.get(view.lookup_url_kwarg or "pk")

        # Ensure the target Order exists, or raise 404
        if not Order.objects.filter(pk=pk).exists():
            raise NotFound(detail="Order not found.")

        # Allow update operations only for business users
        if request.method in ("PUT", "PATCH"):
            return (
                request.user.is_authenticated
                and getattr(request.user, "type", None) == "business"
            )

        # Allow delete operations only for staff users
        if request.method == "DELETE":
            return request.user.is_authenticated and request.user.is_staff

        return False


class IsOfferOwner(BasePermission):
    """
    Ensures only the owning business user can modify an offer.
    Read-only access is granted to any request.
    """

    def has_permission(self, request, view):
        """
        Permit safe (read-only) HTTP methods for any request.
        For write operations, ensure the user is authenticated.

        Args:
            request: The HTTP request being processed.
            view: The view handling the request.

        Returns:
            bool: True if user is authenticated, False otherwise.
        """
        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Permit safe (read-only) HTTP methods for any request.
        For write operations, ensure the requesting user is the owner of the offer object.

        Args:
            request: The HTTP request being processed.
            view: The view handling the request.
            obj: The offer object being accessed.

        Returns:
            bool: True if user is the business_user on the offer, False otherwise.
        """
        if request.method in SAFE_METHODS:
            return True

        return obj.business_user == request.user
