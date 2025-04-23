from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Location
from .serializers import LocationWithBundlesSerializer
import geopy.distance


class NearbyBundlesAPIView(APIView):
    def get(self, request):
        try:
            user_lat = float(request.query_params.get('lat'))
            user_lng = float(request.query_params.get('lng'))
        except (TypeError, ValueError):
            return Response({"error": "Invalid or missing lat/lng"}, status=status.HTTP_400_BAD_REQUEST)

        radius = float(request.query_params.get('radius'))  # meter
        nearby_locations = []

        for location in Location.objects.all():
            coords_user = (user_lat, user_lng)
            coords_loc = (location.lat, location.lng)
            distance = geopy.distance.geodesic(coords_user, coords_loc).meters

            if distance <= radius:
                nearby_locations.append(location)

        serializer = LocationWithBundlesSerializer(nearby_locations, many=True)
        return Response({"results": serializer.data})
