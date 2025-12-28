from django.db import models
from rest_framework.views import APIView
from django.core.serializers.json import DjangoJSONEncoder
import json
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from campaign.models import WeeklyEvent, WeeklyUserScore
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
from django.utils import timezone
from django.db import transaction


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

        profiles = Profile.objects.all().order_by("-total_score")[:5]

        unity_data = {
            "type": "sendUnitsData",
            "data": bundles_data
        }

        unity_data_json = json.dumps(unity_data, cls=DjangoJSONEncoder)

        context = {
            'unity_data': unity_data_json,
            'user_score': total_score,
            'profiles': profiles
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

        try:
            current_event = WeeklyEvent.objects.get(is_active=True)
            if current_event.end_time < timezone.now():
                return JsonResponse({'status': 'error', 'message': 'Active event has ended. Processing rewards...'},
                                    status=400)
        except WeeklyEvent.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'No active weekly event is running'}, status=400)

        try:
            with transaction.atomic():
                user = request.user
                user_profile = user.profile
                points_to_add = asset_bundle.points_per_tap

                # پیدا کردن یا ایجاد رکورد امتیاز هفتگی کاربر برای رویداد فعلی
                weekly_score_record, created = WeeklyUserScore.objects.get_or_create(
                    user=user,
                    event=current_event,
                    defaults={'score': points_to_add}
                )

                if not created:
                    # بهینه‌سازی: استفاده از F() Expression برای به‌روزرسانی اتمی
                    weekly_score_record.score = F('score') + points_to_add
                    weekly_score_record.save(update_fields=['score'])
                    # برای دسترسی به مقدار به‌روز شده، باید دوباره از دیتابیس خوانده شود
                    weekly_score_record.refresh_from_db()

                # Profile Update
                user_profile = request.user.profile
                user_profile.total_score += asset_bundle.points_per_tap
                user_profile.save()

                # check cashable score
                cashout_threshold = 10000
                show_cashout_popup = False

                if user_profile.cashable_score >= cashout_threshold:
                    show_cashout_popup = True

                user_profile.refresh_from_db()

                updated_asset_bundles = AssetBundle.objects.filter(
                    required_score_to_show__lte=user_profile.total_score
                ).order_by('required_score_to_show')

                updated_bundle_urls = [bundle.file_url for bundle in updated_asset_bundles]

        except Exception as e:
            # در صورت بروز هر گونه خطا در تراکنش
            return JsonResponse({'status': 'error', 'message': f'Database update failed: {str(e)}'}, status=500)

        response_data = {
            'status': 'success',
            'user_score': user_profile.total_score,
            'user_weekly_score': weekly_score_record.score,
            'cashable_score': user_profile.cashable_score,
            'show_cashout_popup': show_cashout_popup,
            'asset_bundles': updated_bundle_urls,
        }

        return JsonResponse(response_data)


@method_decorator(login_required, name='dispatch')
class SetCashableScoreView(View):
    def post(self, request, *args, **kwargs):
        try:
            user_profile = request.user.profile
            user_profile.cashable_score = 1
            user_profile.save()

            return JsonResponse({'status': 'success', 'message': 'Cashable score has been reset to 1.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'An error occurred: {str(e)}'}, status=500)


@method_decorator(login_required, name='dispatch')
class LeaderBoardView(View):
    def get(self, request, *args, **kwargs):
        all_profiles = Profile.objects.all().order_by("-total_score", "updated_at")

        # گرفتن 6 پروفایل برتر
        top_profiles = list(all_profiles[:6])

        # اگر کاربر لاگین کرده، رتبه‌اش را پیدا کن
        user_rank = None
        if request.user.is_authenticated:
            try:
                user_profile = Profile.objects.get(user=request.user)
                # پیدا کردن رتبه کاربر در لیست کامل
                user_rank = all_profiles.filter(
                    models.Q(total_score__gt=user_profile.total_score) |
                    models.Q(total_score=user_profile.total_score, updated_at__lt=user_profile.updated_at)
                ).count() + 1
            except Profile.DoesNotExist:
                user_rank = None

        context = {
            "profiles_1": top_profiles[0] if len(top_profiles) > 0 else None,
            "profiles_2": top_profiles[1] if len(top_profiles) > 1 else None,
            "profiles_3": top_profiles[2] if len(top_profiles) > 2 else None,
            "profiles": top_profiles[3:6] if len(top_profiles) > 3 else [],
            "user_rank": user_rank,
        }
        return render(request, 'game/leaderboard.html', context)


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


def settings_view(request):
    return render(request, "game/settings.html")


def selected_games_view(request):
    return render(request, "game/selected.html")
