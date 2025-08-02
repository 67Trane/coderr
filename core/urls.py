"""
URL configuration for the Freelancer project.

This module defines the top-level URL routing for all installed Django apps and the admin interface.

Patterns:
    - Admin site under '/admin/'.
    - REST API endpoints prefixed with '/api/' for Profile, Orders, Offers, Reviews, Authentication, and Core apps.
    - DRF browsable API login under '/api-auth/'.

Each included application defines its own URL patterns under the shared '/api/' namespace.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin interface
    path("admin/", admin.site.urls),
    # Profile app API endpoints
    path("api/", include("profile_app.api.urls")),
    # Orders app API endpoints
    path("api/", include("orders_app.api.urls")),
    # Offers app API endpoints
    path("api/", include("offers_app.api.urls")),
    # Reviews app API endpoints
    path("api/", include("reviews_app.api.urls")),
    # Authentication app API endpoints (registration, login)
    path("api/", include("authentication_app.api.urls")),
    # DRF browsable API login/logout
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # Core app API endpoints
    path("api/", include("core.api.urls")),
]
