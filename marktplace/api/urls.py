from django.urls import path
from .views import *


urlpatterns = [
    path("orders/", OrderListView.as_view(), name="orders"),
]
