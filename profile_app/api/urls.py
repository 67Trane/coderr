from django.urls import path
from .views import (
    ProfileListView,
    ProfileDetailView,
    ProfileTypeListView,
)


urlpatterns = [
    path("profiles/", ProfileListView.as_view(), name="profiles"),
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),
    path(
        "profiles/<str:profile_type>/",
        ProfileTypeListView.as_view(),
        name="profile-by-type",
    ),
]
