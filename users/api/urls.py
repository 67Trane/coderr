from django.urls import path
from .views import UserView, RegistrationView, ProfileView


urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("registration/", RegistrationView.as_view(), name="registration"),
]
