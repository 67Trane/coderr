from django.urls import path
from .views import *


urlpatterns = [
    path("base-info/", BaseInfos.as_view(), name="base-infos"),
]
