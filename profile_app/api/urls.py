from django.urls import path
from .views import (
    ProfileListView,
    ProfileDetailView,
    ProfileTypeListView,
)

"""
URL patterns for the profile_app API.

Defines REST endpoints under the '/api/' prefix for managing user profiles and filtering by user type.

Endpoints:
    GET, POST   /api/profiles/                    -> ProfileListView: List all profiles or create a new profile.
    GET, PUT, PATCH  /api/profile/<pk>/           -> ProfileDetailView: Retrieve or update the authenticated user's own profile.
    GET          /api/profiles/<profile_type>/   -> ProfileTypeListView: List profiles filtered by user type ('business' or 'customer').

Naming conventions:
    'profiles'             - Collection endpoint for profile resources.
    'profile-detail'       - Detail endpoint for individual profile operations.
    'profile-by-type'      - Endpoint for filtering profiles by associated user type.

Permissions:
    - ProfileListView: AllowAny (public access).
    - ProfileDetailView: IsAuthenticated (users may only edit their own profile).
    - ProfileTypeListView: IsAuthenticated (filtering by type requires authentication).
"""
urlpatterns = [
    # List existing profiles or create a new profile
    path("profiles/", ProfileListView.as_view(), name="profiles"),
    # Retrieve or update the authenticated user's profile by ID
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),
    # List profiles for a specific user type (business or customer)
    path(
        "profiles/<str:profile_type>/",
        ProfileTypeListView.as_view(),
        name="profile-by-type",
    ),
]
