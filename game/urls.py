from django.urls import path
from .views import NearbyBundlesAPIView

app_name = "game"
urlpatterns = [
    # version 1
    path("v1/bundles/nearby/", NearbyBundlesAPIView.as_view(), name="bundles-nearby")

    # version 2
]
