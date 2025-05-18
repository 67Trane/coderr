
# from django.urls import path
# from .views import BusinessProfileView


# urlpatterns = [
#     path("profile/", BusinessProfileView.as_view(), name="profile"),
# ]


from rest_framework.routers import DefaultRouter
from .views import BusinessProfileView

router = DefaultRouter()
router.register(r'profile', BusinessProfileView, basename='businessprofile')

urlpatterns = router.urls