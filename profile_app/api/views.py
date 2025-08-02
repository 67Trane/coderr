from profile_app.models import Profile
from .serializers import ProfileSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response

"""
API views for profile_app, managing listing, retrieval, creation, and updating of user profiles.

Views:
    ProfileListView: List all profiles or create a new profile.
    ProfileDetailView: Retrieve or update a single profile with ownership check.
    ProfileTypeListView: List profiles filtered by associated user type.
"""


class ProfileListView(generics.ListCreateAPIView):
    """
    GET: List all Profile instances.
    POST: Create a new Profile instance.

    Permissions:
        AllowAny: Publicly accessible for listing and creation.

    Serializer:
        ProfileSerializer for both read and write operations.
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    GET: Retrieve a single Profile by primary key.
    PUT/PATCH: Update the authenticated user's own Profile.

    Permissions:
        IsAuthenticated: Only logged-in users may access.

    Custom behavior:
        update: Only allow updates if the request.user.profile.id matches the pk.
        Otherwise responds with 403 Forbidden.
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """
        Override update to enforce that users may only edit their own profile.

        Args:
            request: HTTP request containing update data.
            args, kwargs: View arguments including 'pk'.

        Returns:
            Response: Updated profile data or 403 error if unauthorized.
        """
        if request.user.profile.id == int(kwargs.get("pk")):
            return super().update(request, *args, **kwargs)

        return Response(
            {"detail": "Du darfst nur dein eigenes Profil bearbeiten."},
            status=status.HTTP_403_FORBIDDEN,
        )


class ProfileTypeListView(generics.ListAPIView):
    """
    GET: List all profiles filtered by the associated user's type.

    Permissions:
        IsAuthenticated: Only logged-in users may access.

    URL Params:
        profile_type (str): User type to filter profiles (e.g., 'business', 'customer').

    Returns:
        List of ProfileSerializer data for users of the given type.
    """

    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter profiles by the related User's type attribute.

        Returns:
            QuerySet[Profile]: Profiles matching the given profile_type.
        """
        profile_type = self.kwargs.get("profile_type")
        return Profile.objects.filter(user__type=profile_type)
