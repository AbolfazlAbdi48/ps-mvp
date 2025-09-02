from rest_framework.views import APIView
from django.core.serializers.json import DjangoJSONEncoder
import json
from rest_framework.response import Response
from rest_framework import status
from .models import Location
from .serializers import LocationWithBundlesSerializer
import geopy.distance

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

from account.models import Profile
from .models import AssetBundle


def main(request):
    if request.user.is_authenticated:
        return redirect("game:game-play")
    return redirect("account:otp-login")


@method_decorator(login_required, name='dispatch')
class GameplayView(View):
    def get(self, request, *args, **kwargs):
        """
        Load AssetBundles and Run GamePlay.
        """
        total_score = 0
        # Check User Score
        if request.user.is_authenticated:
            user_profile = request.user.profile
            total_score = user_profile.total_score

        asset_bundles = AssetBundle.objects.filter(
            required_score_to_show__lte=total_score
        ).order_by(
            'required_score_to_show'
        )

        bundles_data = [
            {
                "id": str(bundle.id),
                "name": bundle.name,
                "url": request.build_absolute_uri(bundle.file_url)
            }
            for bundle in asset_bundles
        ]

        unity_data = {
            "type": "sendUnitsData",
            "data": bundles_data
        }

        unity_data_json = json.dumps(unity_data, cls=DjangoJSONEncoder)

        context = {
            'unity_data': unity_data_json,
            'user_score': total_score,
        }

        return render(request, 'game/play.html', context)

    def post(self, request, *args, **kwargs):
        """
        JS API
        """
        # POST data from JS
        # tapped bundles ID
        # request_data = request.POST.get('tapped_asset')
        tapped_asset_name = request.POST.get('tapped_asset_id')

        try:
            asset_bundle = AssetBundle.objects.get(id=tapped_asset_name)
        except AssetBundle.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Asset not found'}, status=404)

        # Profile Update
        user_profile = request.user.profile
        user_profile.total_score += asset_bundle.points_per_tap
        user_profile.save()

        # check cashable score
        cashout_threshold = 10000
        show_cashout_popup = False

        if user_profile.cashable_score >= cashout_threshold:
            show_cashout_popup = True

        # load asset bundles
        updated_asset_bundles = AssetBundle.objects.filter(
            required_score_to_show__lte=user_profile.total_score).order_by('required_score_to_show')
        updated_bundle_urls = [bundle.file_url for bundle in updated_asset_bundles]

        response_data = {
            'status': 'success',
            'user_score': user_profile.total_score,
            'cashable_score': user_profile.cashable_score,
            'show_cashout_popup': show_cashout_popup,
            'asset_bundles': updated_bundle_urls,
        }

        return JsonResponse(response_data)


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
