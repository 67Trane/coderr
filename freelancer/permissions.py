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
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

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
