from django.urls import path
from .views import (
    UserView,
    UserDetailView,
    RegistrationView,
    ProfileListView,
    ProfileDetailView,
    ProfileTypeListView,
    LoginView,
)


urlpatterns = [
    path("profiles/", ProfileListView.as_view(), name="profiles"),
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),
    path(
        "profiles/<str:profile_type>/",
        ProfileTypeListView.as_view(),
        name="profile-by-type",
    ),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("base-info/", UserDetailView.as_view(), name="user"),
    path("login/", LoginView.as_view(), name="login"),
]
