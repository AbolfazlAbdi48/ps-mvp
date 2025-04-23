from django.urls import path
from .views import NearbyBundlesAPIView

app_name = "game"
urlpatterns = [
    path("bundles/nearby/", NearbyBundlesAPIView.as_view(), name="bundles-nearby")
]
