from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCustomerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.type == "customer"


class IsReviewer(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.reviewer == request.user


class IsBusinessOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.type == "business"


class IsBusinessForUpdateOrAdminForDelete(BasePermission):
    """
    - SAFE_METHODS (GET, HEAD, OPTIONS) are always allowed.
    - PUT/PATCH only if the order exists AND user.type == 'business'
    - DELETE only if the order exists AND user.is_staff
    """

    def has_permission(self, request, view):
        # 1) Always allow read‐only
        if request.method in SAFE_METHODS:
            return True

        # 2) Grab the PK from the URL
        pk = view.kwargs.get(view.lookup_url_kwarg or "pk")
        
        # 3) Existence check
        if not Order.objects.filter(pk=pk).exists():
            # raises a 404 immediately, before any 403
            raise NotFound(detail="Order not found.")

        # 4) Now your method‐specific checks
        if request.method in ("PUT", "PATCH"):
            return (
                request.user.is_authenticated
                and getattr(request.user, "type", None) == "business"
            )
        
        if request.method == "DELETE":
            return request.user.is_authenticated and request.user.is_staff

        return False


class IsOfferOwner(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.business_user == request.user
