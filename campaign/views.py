from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import UserProgress, Campaign
from rest_framework.generics import ListAPIView
from .serializers import LeaderboardSerializer

User = get_user_model()


class AddScoreView(APIView):
    def post(self, request):
        username = request.data.get('username')
        campaign_id = request.data.get('campaign_id')
        score = request.data.get('score', 0)

        if not username or not campaign_id:
            return Response({'error': 'username و campaign_id الزامی هستند.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            campaign = Campaign.objects.get(id=campaign_id)
        except User.DoesNotExist:
            return Response({'error': 'کاربر پیدا نشد.'}, status=status.HTTP_404_NOT_FOUND)
        except Campaign.DoesNotExist:
            return Response({'error': 'کمپین پیدا نشد.'}, status=status.HTTP_404_NOT_FOUND)

        progress, created = UserProgress.objects.get_or_create(user=user, campaign=campaign)
        progress.score += int(score)
        progress.save()

        return Response({'message': 'امتیاز با موفقیت ثبت شد.', 'total_score': progress.score},
                        status=status.HTTP_200_OK)


class LeaderboardView(ListAPIView):
    queryset = UserProgress.objects.order_by('-score')[:20]
    serializer_class = LeaderboardSerializer
