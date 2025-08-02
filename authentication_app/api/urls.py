from django.urls import path
from .views import RegistrationView, LoginView

"""
URL patterns for the authentication_app API.

Defines endpoints for user registration and login under the '/api/' prefix.

Endpoints:
    POST /api/registration/  -> RegistrationView: Create a new user and obtain auth token.
    POST /api/login/         -> LoginView: Authenticate an existing user and return auth token.

Names:
    'registration' - Named URL for client library reference or reverse lookups.
    'login'        - Named URL for the login endpoint.
"""
urlpatterns = [
    # Register a new user and receive authentication token
    path("registration/", RegistrationView.as_view(), name="registration"),
    # Authenticate existing user and receive authentication token
    path("login/", LoginView.as_view(), name="login"),
]
