from django.urls import path
from .views import ProfileView, RegistrationView


urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("registration/", RegistrationView.as_view(), name="registration")
]
